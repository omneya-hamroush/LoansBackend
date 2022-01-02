from rest_framework import serializers
from userApp import models






class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = "__all__"

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class CustomerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerUser
        fields = "__all__"

        
