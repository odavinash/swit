# Generated by Django 2.0.2 on 2019-04-01 16:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discount_coupons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcoupon',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
