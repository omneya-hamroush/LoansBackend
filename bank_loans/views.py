from django.shortcuts import render
from bank_loans import models, serializers
from userApp import models as userModels
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from BankLoans import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from numpy_financial import pmt
# from django.utils import simplejson
import json
from django.http import HttpResponse
from rest_framework import status


# function to return all the data for the amortization table
def amortization(rate, amount, monthly_payment, term):
    monthly_rate = rate/12
    balance = amount
    print("vvvvvvvvvvv")
    print(balance)
    x = []
    i = 0
    while balance > 0:
        l = {}
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance = balance - principal
        l = {"Month":i+1, "Payment":monthly_payment, "Interest":interest, "principal":principal, "Balance":balance}
        x.append(l)
        i = i + 1
    return x

# to get all the funds that the amount is within
class GetFunds(APIView):
    # permission_classes = (permissions.ProviderPermission,)
    # authentication_classes = (TokenAuthentication,)
    def get(self,request):
        amount = self.request.query_params.get('amount')
        queryset = models.Fund.objects.all()
        queryset = queryset.filter(minimum__lte=amount, maximum__gte=amount)
        serializer = serializers.FundSerializer(queryset, many=True,context={'request':request})
        print(serializer.data)
        if serializer.data == []:
            return Response({"No matching funds"})
        else:

            return Response({"data": serializer.data})


# to return amortization table for the fund
class FundAmort(APIView):
    # permission_classes = (permissions.ProviderPermission,)
    # authentication_classes = (TokenAuthentication,)
    def get(self,request):
        fund_id = self.request.query_params.get('fund_id')
        amount = self.request.query_params.get('amount')
        loan_id = self.request.query_params.get('loan_id')
        if(fund_id is not None):
            fund = models.Fund.objects.get(id=fund_id)
            print("cccccccccc")
            print(fund)
            print(type(int(amount)))
            print(type(fund.interest_rate))
            print(type(12))
            print("xxxxxxxxxxx")
            months = fund.duration * 12
            print(months)
            rate = (fund.interest_rate / 100)
            print(rate)
            amount = int(amount)
            payment = -(pmt(rate/12, months, amount))
            print(payment)
            table = amortization(rate, amount, payment, months)
            print(table)
            amort_table = json.dumps({"amortization_table" : table})
            return HttpResponse(amort_table, content_type ="application/json")
        if(loan_id is not None):
            loan = models.Loan.objects.get(id=loan_id)
            print("cccccccccc")
            print(loan)
            print(type(int(amount)))
            print(type(loan.interest_rate))
            print(type(12))
            print("xxxxxxxxxxx")
            months = loan.duration * 12
            print(months)
            rate = (loan.interest_rate / 100)
            print(rate)
            amount = int(amount)
            payment = -(pmt(rate/12, months, amount))
            print(payment)
            table = amortization(rate, amount, payment, months)
            print(table)
            amort_table = json.dumps({"amortization_table" : table})
            return HttpResponse(amort_table, content_type ="application/json")






class AddFundApplication(APIView):
    # permission_classes = (permissions.ProviderPermission,)
    # authentication_classes = (TokenAuthentication, IsAuthenticated)
    def post(self,request):
        data = json.loads(request.body)
        print("---------")
        print(data)
        print("---------")
        fund_id = data["fund_id"]
        amount = data["amount"]
        user = data["user_id"]
        # fund_id = self.request.query_params.get('fund_id')
        fund = models.Fund.objects.get(id=fund_id)
        print(fund_id)
        print("ccccccccc")
        # amount = self.request.query_params.get('amount')
        print("iiiiiiiiiiiiii")
        # print(type(amount))
        # print(amount)
        # print(self.request.user.id)
        user = userModels.User.objects.get(id=user)
        print(user.is_loan_provider)

        # fund_data = {"amount":amount, "fund":fund_id,
        # }
        fund_application = models.FundApplication.objects.create(
          amount=amount, fund=fund, user=user
        )
        # fund.save(using=self._db)
        serializer = serializers.FundApplicationSerializer(fund_application, context={'request':request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetFundApplications(APIView):
    # permission_classes = (permissions.ProviderPermission,)
    # authentication_classes = (TokenAuthentication,)
    def get(self,request):
        user_id = self.request.query_params.get("user_id")
        user = userModels.User.objects.get(id=user_id)
        queryset = models.FundApplication.objects.all()
        print(user)
        queryset = queryset.filter(user=user_id)
        serializer = serializers.FundApplicationSerializer(queryset, many=True,context={'request':request})
        print(serializer.data)
        if serializer.data == []:
            return Response({"No Applications found"})
        else:

            return Response({"data": serializer.data})



class GetLoanApplications(APIView):
    # permission_classes = (permissions.ProviderPermission,)
    # authentication_classes = (TokenAuthentication,)
    def get(self,request):
        user_id = self.request.query_params.get("user_id")
        user = userModels.User.objects.get(id=user_id)
        queryset = models.LoanApplication.objects.all()
        print(user)
        queryset = queryset.filter(user=user_id)
        serializer = serializers.LoanApplicationSerializer(queryset, many=True,context={'request':request})
        print(serializer.data)
        if serializer.data == []:
            return Response({"No Applications found"})
        else:

            return Response({"data": serializer.data})




class GetLoans(APIView):
    # permission_classes = (permissions.CustomerPermission,)
    # authentication_classes = (TokenAuthentication,)
    def get(self,request):
        amount = self.request.query_params.get('amount')
        queryset = models.Loan.objects.all()
        queryset = queryset.filter(minimum__lte=amount, maximum__gte=amount)
        serializer = serializers.LoanSerializer(queryset, many=True,context={'request':request})
        print(serializer.data)
        if serializer.data == []:
            return Response({"No matching loans"})
        else:

            return Response({"data": serializer.data})




# returns all the available loans durations
class GetLoanTerms(APIView):
    authentication_classes = (TokenAuthentication,)
    def get(self,request):
        queryset = models.Loan.objects.all()
        x = []
        for i in queryset:
            x.append(i.duration)
        l = list( dict.fromkeys(x) )
        return Response(l)


class AddLoanApplication(APIView):
    # permission_classes = (permissions.CustomerPermission,)
    # authentication_classes = (TokenAuthentication,)
    def post(self,request):
        data = json.loads(request.body)
        print("---------")
        print(data)
        print("---------")
        loan_id = data["loan_id"]
        amount = data["amount"]
        user = data["user_id"]
        # loan_id = self.request.query_params.get('loan_id')
        print("---------")
        print(loan_id)

        # amount = self.request.query_params.get('amount')
        print("xxxxxxxxx")
        print(self.request.user.id)
        loan = models.Loan.objects.get(id=loan_id)
        print("ppppppppp")
        print(loan)
        user = userModels.User.objects.get(id=user)

        print(user)
        if(int(loan.minimum) <= int(amount) and int(loan.maximum) >= int(amount)):
            loan_application = models.LoanApplication.objects.create(
              amount=amount, loan=loan, user=user
            )
            # fund.save(using=self._db)
            serializer = serializers.LoanApplicationSerializer(loan_application, context={'request':request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"Amount is not within the range of the loan."})




class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LoanSerializer
    queryset = models.Loan.objects.all()
    # permission_classes = (permissions.PersonnelPermission,)
    # authentication_classes = (TokenAuthentication,)
    def create (self, request, *args, **kwargs):
        data = json.loads(request.body)
        # print("---------")
        # print(data)
        # print("---------")
        minimum = data["minimum"]
        maximum = data["maximum"]

        # minimum = request.data.get("minimum")
        # maximum = request.data.get("maximum")
        funds = models.Fund.objects.count()
        loans = models.Loan.objects.count()
        print(funds, loans)
        if int(minimum) >= int(maximum):
            return Response({"Minimum cannot exceed maximum"})
        if loans >= funds:
            return Response({"you cannot add any more loans"})
        else:
            print(type(minimum), type(maximum))
            print("iuiuiuiuiuiuiuiuiuiu")
            return super().create(request, *args, **kwargs)



class FundViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FundSerializer
    queryset = models.Fund.objects.all()
    # permission_classes = (permissions.PersonnelPermission,)
    # authentication_classes = (TokenAuthentication,)
    def create (self, request, *args, **kwargs):
        data = json.loads(request.body)
        print("---------")
        print(data)
        print("---------")
        minimum = data["minimum"]
        maximum = data["maximum"]
        # rate = data["rate"]
        # duration = data["duration"]
        # minimum = self.request.query_params.get("minimum")
        # maximum = self.request.query_params.get("maximum")
        # rate = self.request.query_params.get('interest_rate')
        # duration = self.request.query_params.get('duration')
        print(minimum)
        if int(minimum) >= int(maximum):
            print("HEREEEEE")
            return Response({"Minimum cannot exceed maximum"})
        else:
            return super().create(request, *args, **kwargs)
            # fund = models.Fund.objects.create(
            #   minimum=minimum, maximum=maximum, interest_rate=rate, duration=duration
            # )
            # # fund.save(using=self._db)
            # serializer = serializers.FundSerializer(fund, context={'request':request})
            # return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoanApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LoanApplicationSerializer
    queryset = models.LoanApplication.objects.all()
    # permission_classes = (permissions.PersonnelPermission,)
    # authentication_classes = (TokenAuthentication,)



class FundApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FundApplicationSerializer
    queryset = models.FundApplication.objects.all()
    # permission_classes = (permissions.PersonnelPermission,)
    # authentication_classes = (TokenAuthentication,)
