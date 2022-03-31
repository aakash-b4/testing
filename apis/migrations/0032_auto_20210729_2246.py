# Generated by Django 3.2.4 on 2021-07-29 17:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0031_auto_20210729_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 777110)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 839633)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 823988)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 792733)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 792733)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 808357)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 823988)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 777110)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 808357)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 823988)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 808357)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 808357)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 846142)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 792733)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='credit_transaction_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 792733), null=True),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='trans_init_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 29, 22, 46, 16, 823988)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 7, 29, 22, 46, 16, 846142)),
        ),
    ]
