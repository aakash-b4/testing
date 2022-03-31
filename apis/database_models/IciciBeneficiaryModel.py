from django.db import models
import uuid


class ICICI_Beneficiary(models.Model):
    id = models.AutoField(primary_key=True)
    merchantId = models.CharField(max_length=100, blank=True, null=True)
    payout_beneficiary_id = models.CharField(
        max_length=10, blank=True, null=True)
    aggrId = models.CharField(max_length=100, blank=True, null=True)
    corpId = models.CharField(max_length=100, blank=True, null=True)
    corpUsr = models.CharField(max_length=100, blank=True, null=True)
    payeeType = models.CharField(max_length=2, null=True)
    bnfId = models.CharField(max_length=100, blank=True, null=True)
    URN = models.CharField(null=True, max_length=50)
    ifsc_registered = models.BooleanField(default=False)
    vpa_registered = models.BooleanField(default=False)
    errorMessage = models.CharField(max_length=100, blank=True, null=True)
    response = models.CharField(max_length=100, blank=True, null=True)
    success = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=500, null=True)
    errorCode = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, null=True)
    updated_by = models.CharField(max_length=100, null=True)

    # function to convert the json to class object

    @staticmethod
    def from_json(json_beneficiary):
        return ICICI_Beneficiary(
            id=json_beneficiary.get('id', None),
            merchantId=json_beneficiary.get('merchantId', None),
            aggrId=json_beneficiary.get('AGGR_ID', None),
            corpId=json_beneficiary.get('CrpId', None),
            corpUsr=json_beneficiary.get('CrpUsr', None),
            payeeType=json_beneficiary.get('PayeeType', None),
            bnfId=json_beneficiary.get('bnfId', None),
            URN=json_beneficiary.get('URN', None),
            errorMessage=json_beneficiary.get('errorMessage', None),
            response=json_beneficiary.get('response', None),
            success=json_beneficiary.get('success', None),
            status=json_beneficiary.get('status', None),
            message=json_beneficiary.get('message', None),
            errorCode=json_beneficiary.get('errorCode', None),
            created_at=json_beneficiary.get('created_at', None),
            deleted_at=json_beneficiary.get('deleted_at', None),
            updated_at=json_beneficiary.get('updated_at', None),
            created_by=json_beneficiary.get('created_by', None),
            updated_by=json_beneficiary.get('updated_by', None),
        )

    # function to convert the objet to json

    def to_json(self):
        return {
            'id': self.id,
            'merchantId': self.merchantId,
            'aggrId': self.aggrId,
            'corpId': self.corpId,
            'corpUsr': self.corpUsr,
            'payeeType': self.payeeType,
            'bnfId': self.bnfId,
            'URN': self.URN,
            'errorMessage': self.errorMessage,
            'response': self.response,
            'success': self.success,
            'status': self.status,
            'message': self.message,
            'errorCode': self.errorCode,
            'created_at': self.created_at,
            'deleted_at': self.deleted_at,
            'updated_at': self.updated_at,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
        }
