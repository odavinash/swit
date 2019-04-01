from django.contrib.auth import authenticate
from rest_framework import serializers
from discount_coupons.mixins import UserSerializer
from . import models


class LoginSerializer(UserSerializer, serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = (
            'username',
            'password'
            )

    def validate(self, data):
        user = authenticate(
            self.context['request'],
            username=data.get('username'),
            password=data.get('password'),
        )
        print(data.get('username'))
        if not user:
        	print(user)
        else:
        	print(user)

        self.user = user

        return data
        

class DiscountCouponSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= models.DiscountCoupon
        
        fields = (
            'user',
            'product',
            'code_coupons',
            'exp_date',
            )


class ApplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model= models.DiscountCoupon
        
        fields = (
            'user',
            'product',
            'code_coupons',
            'exp_date',
            'discount_applied',
            'price',
            )