# Generated by Django 4.0.1 on 2022-01-18 05:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0085_icici_beneficiary_alter_bankpartnermodel_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='icici_beneficiary',
            name='aggrName',
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 764146)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 786119)),
        ),
        migrations.AlterField(
            model_name='bousermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 784148)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 770118)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 768147)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 773117)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 779150)),
        ),
        migrations.AlterField(
            model_name='mercahantmodemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 791117)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 763148)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 778117)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 781120)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 776151)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 775117)),
        ),
        migrations.AlterField(
            model_name='slabmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 788149)),
        ),
        migrations.AlterField(
            model_name='taxmodel',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 797118)),
        ),
        migrations.AlterField(
            model_name='transactionhistorymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 766118)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 783149)),
        ),
        migrations.AlterField(
            model_name='webhookmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 18, 10, 46, 35, 789154)),
        ),
    ]
