# Generated by Django 4.2.1 on 2023-08-02 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_account_cust_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrequest',
            name='cust_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
