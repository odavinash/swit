# Generated by Django 2.0.2 on 2019-04-01 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discount_coupons', '0002_discountcoupon_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discountcoupon',
            old_name='date',
            new_name='exp_date',
        ),
    ]
