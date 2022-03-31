# Generated by Django 3.2.9 on 2022-03-03 07:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0101_merge_20220303_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiarymodel',
            name='category',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='cibregistration',
            name='bank',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apis.bankpartnermodel'),
        ),
        migrations.AddField(
            model_name='cibregistration',
            name='merchantId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 649087)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 649087)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 665097)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 649087)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 665097)),
        ),
        migrations.AlterField(
            model_name='taxmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 665097)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 649087)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 657082)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 3, 13, 16, 14, 665097)),
        ),
    ]
