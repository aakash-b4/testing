# Generated by Django 3.2 on 2021-07-13 07:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0005_auto_20210713_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='BOUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField()),
                ('username', models.CharField(max_length=300)),
                ('password', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=300)),
                ('email', models.EmailField(default=None, max_length=254, null=True)),
                ('mobile', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 586127))),
                ('updated_at', models.DateTimeField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('created_by', models.CharField(default=None, max_length=300, null=True)),
                ('updated_by', models.CharField(default=None, max_length=300, null=True)),
                ('deleted_by', models.CharField(default=None, max_length=300, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bankpartnermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 23, 266999)),
        ),
        migrations.AlterField(
            model_name='chargemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='featuremodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='ipwhitelistedmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='ledgermodel',
            name='trans_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='logmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 586127)),
        ),
        migrations.AlterField(
            model_name='merchantmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='modemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 586127)),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 586127)),
        ),
        migrations.AlterField(
            model_name='rolefeaturemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 586127)),
        ),
        migrations.AlterField(
            model_name='rolemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 570503)),
        ),
        migrations.AlterField(
            model_name='useractivemodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 13, 12, 38, 22, 586127)),
        ),
    ]
