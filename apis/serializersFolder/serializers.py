from apis.database_models.DailyLedgerModel import DailyLedgerModel
from apis.database_models.BeneficiaryModel import BeneficiaryModel
from apis.database_models.CIBRegistrationModel import CIBRegistration
from django.db.models import fields
from rest_framework import serializers

from apis.database_models.SlabModel import SlabModel
from ..models import LogModel
from ..database_models import LedgerModel
class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerModel
        fields = ("id", "client", "client_code", "amount",
                  "trans_type", "type_status", "bank_ref_no", "customer_ref_no", "bank", "trans_status", "bene_account_name", "bene_account_number", "bene_ifsc", "request_header", "mode", "charge", "trans_time", "van", "created_at", "deleted_at", "updated_at", "createdBy", "updatedBy", "deletedBy","status")


class CreateLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerModel
        fields = ("client", "client_code", "amount",
                  "trans_type", "type_status", "bank_ref_no", "customer_ref_no", "bank", "trans_status", "bene_account_name", "bene_account_number", "bene_ifsc", "request_header", "mode", "charge", "trans_time", "van", "created_at", "deleted_at", "updated_at", "createdBy", "updatedBy", "deletedBy", "status")



class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model=LogModel
        fields="__all__"


class DailyLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model=DailyLedgerModel
        fields="__all__"


class BeneSerializer(serializers.ModelSerializer):
    class Meta:
        model=BeneficiaryModel
        fields=("id","full_name","account_number","ifsc_code","upi_id","merchant_id")
class SlabSerializer(serializers.ModelSerializer):
    class Meta:
        model=SlabModel
        fields="__all__"

class CibRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=CIBRegistration
        fields='__all__'

    # function create
    def create(self, validated_data):
        return CIBRegistration.objects.create(**validated_data)

    # function update
    def update(self, instance, validated_data):
        instance.bank = validated_data.get('bank', instance.bank)
        instance.aggrName = validated_data.get('aggrName', instance.aggrName)
        instance.aggrId = validated_data.get('aggrId', instance.aggrId)
        instance.corpId = validated_data.get('corpId', instance.corpId)
        instance.userId = validated_data.get('userId', instance.userId)
        instance.aliasId = validated_data.get('aliasId', instance.aliasId)
        instance.urn = validated_data.get('urn', instance.urn)
        instance.errormessage = validated_data.get('errormessage', instance.errormessage)
        instance.response = validated_data.get('response', instance.response)
        instance.success = validated_data.get('success', instance.success)
        instance.status = validated_data.get('status', instance.status)
        instance.message = validated_data.get('message', instance.message)
        instance.errorCode = validated_data.get('errorCode', instance.errorCode)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.deleted_at = validated_data.get('deleted_at', instance.deleted_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()
        return instance

    # equals function to check if two objects are equal
    def equals(self, obj1, obj2: dict):
        if obj1.bank == obj2.get('bank') and obj1.aggrName == obj2.get('aggrName') and obj1.aggrId == obj2.get('aggrId') and obj1.corpId == obj2.get('corpId') and obj1.userId == obj2.get('userId') and obj1.aliasId == obj2.get('aliasId') and obj1.merchantAccountNumber == obj2.get('merchantAccountNumber'):
            return True
        else:
            return False