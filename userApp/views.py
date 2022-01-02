from django.shortcuts import render
from userApp import models, serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import time

# class LoginView(TokenObtainPairView):
#     pass


class LoginViewSet(ObtainAuthToken):
    """Checks login creds and returns auth token"""

    # serializer_class = serializers.UserSerializer
    def post(self, request):
        # time.sleep(10)
        user = models.User.objects.filter(email=request.data['username'])
        print("-------------")
        print(type(request.data['username']))
        print(type(request.data['password']))
        # user1 = models.User.objects.get(email=request.data['username'])
        if user:

            user = user[0]
            print(user)

            user.save()
            is_correct_password = user.check_password(
                request.data['password'])
            print("xxxxxxxxxx")
            print(is_correct_password)
            if not user.is_active and is_correct_password:
                tokens = Token.objects.filter(user=user)
                tokens.delete()

                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'id': user.id,
                    'is_active': user.is_active,
                    'is_loan_provider': user.is_loan_provider,
                    'is_loan_customer': user.is_loan_customer,
                    'is_bank_personnel': user.is_bank_personnel,

                })
            if is_correct_password == False:
                return Response({"Incorrect Password"})
            print(user)
            # if user1.is_loan_provider == True:
            #     provider = models.ProviderUser.objects.create(
            #      user=user1
            #      )
            # if user1.is_loan_customer == True:
            #     provider = models.CustomerUser.objects.create(
            #      user=user1
            #      )

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']


        token, created = Token.objects.get_or_create(user=user)
        print(token)
        print("llllllllllllll")
        print(user)
        # if user1.is_loan_provider == True:
        #     provider = models.ProviderUser.objects.create(
        #          user=user1
        #          )
        # if user1.is_loan_customer == True:
        #     provider = models.CustomerUser.objects.create(
        #          user=user1
        #          )
        return Response({
            'token': token.key,
            'id': user.id,
            'is_active': user.is_active,
            'is_loan_provider': user.is_loan_provider,
            'is_loan_customer': user.is_loan_customer,
            'is_bank_personnel': user.is_bank_personnel,

        })


class LogoutView(APIView):
    """
        remove the auth token from the database
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response(
            {
                "details": "Logged out Successfully",
            },
            status=status.HTTP_200_OK)
