# Generated by Django 4.2.4 on 2023-09-10 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customer_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]