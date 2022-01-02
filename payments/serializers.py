from rest_framework import serializers

from payments import models


class PaymentSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Payment
        fields = "__all__"
        # read_only_fields = ('id',)
