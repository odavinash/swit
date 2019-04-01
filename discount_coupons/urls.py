from django.urls import path
from . import views


app_name = 'discount_coupons'


urlpatterns = [
    #api to insert payment id and payment url in order table
    path("login", views.Login.as_view(), name="login"),
    path("get-coupon", views.GetCoupon.as_view(), name="getcoupon"),
    path("apply-coupon<str:code_coupons>", views.ApplyCoupon.as_view(), name="applycoupon"),
    path("payment", views.Payment.as_view(), name="payment"),
]
