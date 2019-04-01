from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics
from discount_coupons import serializers
from discount_coupons import models
from rest_framework import status
import datetime
from django.utils import timezone
from urllib.parse import urlencode, quote_plus
import requests
from django.conf import settings


# Create your views here.


class Login(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.get_data()
            return Response({'message': 'success', 'success': True, 'data': data})
        except Exception as e:
            return Response({'message': format(e.args[-1]), 'success': False})



class GetCoupon(generics.RetrieveAPIView):
    serializer_class = serializers.DiscountCouponSerializer
    permission_classes = (IsAuthenticated,)
    model = models.DiscountCoupon
    queryset = models.DiscountCoupon.objects.all()

    def get_object(self):
    	try:
    		return self.model.objects.get(user=self.request.user)
    	except self.model.DoesNotExist:
    		return None

    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = super(GetCoupon, self).retrieve(request, args, kwargs)
            return Response({"status": 200, 'data': serializer.data})
        except Exception as e:
            return Response ({"status": 400, "message" : "Failure to get coupon"}, status=status.HTTP_400_BAD_REQUEST)


class ApplyCoupon(generics.RetrieveAPIView):
    serializer_class = serializers.ApplySerializer
    permission_classes = (IsAuthenticated,)
    model = models.DiscountCoupon
    queryset = models.DiscountCoupon.objects.all()

    def get_object(self):
    	try:
    		print(self.kwargs['code_coupons'])
    		return self.model.objects.get(user=self.request.user, code_coupons=self.kwargs['code_coupons'])
    	except self.model.DoesNotExist:
    		return None

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            exp_date = instance.exp_date
            
            serializer = self.get_serializer(instance)
            if instance is None:
            	response = {'message': 'Coupon not found for you.', 'success': False}
            else:
            	today = timezone.now()
            
            	if today > exp_date:
            		response = {'message': 'Coupon expired.', 'success': False}
            	else:
            		instance.price = int(instance.price - (instance.price * instance.discount_applied) / 100)
            		response = serializer.data
            	
            return Response({"status": 200, 'data': response})
        except Exception as e:
        	print(e)
        	return Response ({"status": 400, "message" : "Failure to apply coupon"}, status=status.HTTP_400_BAD_REQUEST)


class Payment(generics.RetrieveAPIView):
    serializer_class = serializers.DiscountCouponSerializer
    permission_classes = (IsAuthenticated,)
    model = models.DiscountCoupon
    queryset = models.DiscountCoupon.objects.all()

    def get_object(self):
    	try:
    		obj = self.model.objects.get(user=self.request.user)

    		http_build_query = {'grant_type' : settings.MYFATOORAH_GRANT_TYPE,'username' : settings.MYFATOORAH_USERNAME,'password' : settings.MYFATOORAH_PASSWORD}

    		response = requests.post(
                url=settings.MYFATOORAH_URL,
                headers={
                    "Content-Type": "application/json",
                    "Accept-Charset": "UTF-8"
                },
                data=urlencode(http_build_query, quote_via=quote_plus)
            )

    		data = response.json()

    		if data.get('access_token'):
    			access_token = data.get('access_token')
    		else:
    			access_token = ''

    		if data.get('access_token'):
    			token_type = data.get('token_type')
    		else:
    			token_type = ''
    		print(obj.price)
    		if data.get('access_token'):
    				post_string = """{
			    "InvoiceValue": 10,
			    "CustomerName": "%s",
			    "CustomerBlock": "Block",
			    "CustomerStreet": "Street",
			    "CustomerHouseBuildingNo": "Building no",
			    "CustomerCivilId": "123456789124",
			    "CustomerAddress": "Payment Address",
			    "CustomerReference": "ref",
			    "DisplayCurrencyIsoAlpha": "EUR",
			    "CountryCodeId": "+91",
			    "CustomerMobile": "1234567890",
			    "CustomerEmail": "test@gmail.com",
			    "DisplayCurrencyId": 3,
			    "SendInvoiceOption": 1,
			    "InvoiceItemsCreate": [
			    {
			        "ProductId": null,
			        "ProductName": "%s",
			        "Quantity": 1,
			        "UnitPrice": "100"
			    }
			    ],
			    "CallBackUrl":  "http://www.google.com",
			    "Language": 2,
			    "ExpireDate": "2022-12-31T13:30:17.812Z",
			    "ApiCustomFileds": "weight=10,size=L,lenght=170",
			    "ErrorUrl": "http://www.bing.com"
			}"""%(obj.user, obj.product)

    		response = requests.post(
			    url='https://apidemo.myfatoorah.com/ApiInvoices/CreateInvoiceIso',
			    headers={
			        "Content-Type": "application/json",
			        "Accept-Charset": "UTF-8",
			        "Authorization": "Bearer "+access_token
			    },
			    data=post_string
			)
    		data = response.json()

    		return response
    	except self.model.DoesNotExist:
    		return None

    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = self.get_object()
            return Response({"status": 200, 'data': serializer})
        except Exception as e:
        	print(e)
        	return Response ({"status": 400, "message" : "Failure to get coupon"}, status=status.HTTP_400_BAD_REQUEST)