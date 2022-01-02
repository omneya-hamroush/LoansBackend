from rest_framework import serializers
from bank_loans import models
from userApp import serializers as userSerializers

class FundSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Fund
        fields = "__all__"



class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Loan
        fields = "__all__"


class FundApplicationSerializer(serializers.ModelSerializer):
    user = userSerializers.UserSerializer(read_only=True)
    class Meta:
        model = models.FundApplication
        fields = "__all__"


class LoanApplicationSerializer(serializers.ModelSerializer):
    user = userSerializers.UserSerializer(read_only=True)
    class Meta:
        model = models.LoanApplication
        fields = "__all__"
