# Generated by Django 4.0.1 on 2022-01-29 07:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0096_merchantmodel_account_number_merchantmodel_upi_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MerchantAccountDetail',
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 770952)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 788953)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 786988)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 774989)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 773963)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 777953)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 782997)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 792967)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 768950)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 781952)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 784986)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 780963)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 778988)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 789989)),
        ),
        migrations.AlterField(
            model_name='taxmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 798988)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 771952)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 785986)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 29, 13, 19, 22, 791951)),
        ),
    ]
