from django.db import models
from django.utils import timezone

# Create your models here.


class DiscountCoupon(models.Model):
    class Meta:
        db_table = "discount_coupon"

    id_discount_coupon = models.AutoField(primary_key=True)
    user = models.CharField(max_length=50, null=False,)
    product = models.CharField(max_length=50, null=False)
    code_coupons = models.CharField(max_length=50, null=False)
    price = models.IntegerField(null=False)
    discount_applied = models.IntegerField(null=False)
    exp_date = models.DateTimeField(null=False, default=timezone.now)
