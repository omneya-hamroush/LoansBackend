from django.shortcuts import render
from django.shortcuts import render
from payments import models, serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from BankLoans import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from numpy_financial import pmt
# from django.utils import simplejson
from datetime import datetime
from numpy_financial import pmt
import json
from django.http import HttpResponse
from rest_framework import status
from bank_loans import models as loanModels
from userApp import models as userModels
from django.utils import timezone
from datetime import datetime, timedelta


class GetPayments(APIView):
    def get(self,request):
        user_id = self.request.query_params.get("user_id")
        queryset = models.Payment.objects.all()
        queryset = queryset.filter(user=user_id)
        serializer = serializers.PaymentSerializer(queryset, many=True,context={'request':request})
        return Response({"data": serializer.data})


class AddPayment(APIView):
    def post(self,request):
        data = json.loads(request.body)
        print("---------")
        print(data)
        print("---------")
        application_id = data["loanapp_id"]
        application_id = self.request.query_params.get('loanapp_id')
        user_id = data["user_id"]
        user = userModels.User.objects.get(id=user_id)
        loan_app = loanModels.LoanApplication.objects.get(id=application_id)
        loan_app.status = "approved"
        loan_app.save()
        print(loan_app.loan.minimum)
        amount = loan_app.amount
        months = loan_app.loan.duration * 12
        print(months)
        rate = (loan_app.loan.interest_rate / 100)
        print(loan_app.status)
        payment = -(pmt(rate/12, months, amount))
        print(payment)
        deadline = datetime.now()+timedelta(days=30)
        payment = models.Payment.objects.create(user=user, status="Pending", title="Monthly payment", total=payment, date_of_deadline=deadline)
        serializer = serializers.PaymentSerializer(payment, context={'request':request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApproveFund(APIView):
    def post(self,request):
        data = json.loads(request.body)
        print("---------")
        print(data)
        print("---------")
        application_id = data["fundapp_id"]
        # application_id = self.request.query_params.get('fundapp_id')

        fund_app = loanModels.FundApplication.objects.get(id=application_id)
        fund_app.status = "approved"
        fund_app.save()
        print(fund_app.status)

        # serializer = serializers.PaymentSerializer(payment, context={'request':request})
        return Response({"Fund approved"})
