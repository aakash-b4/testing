from django.db import connection
from ..database_models.MerchantModeModel import MercahantModeModel
from apis.database_models.MerchantModeModel import MercahantModeModel
from datetime import datetime
class Merchant_Mode_Service:
    def __init__(self,merchant_id,bank_partner_id,mode_id):
        self.merchant_id=merchant_id
        self.bank_partner_id=bank_partner_id
        self.mode_id=mode_id
    def save(self):
        merchant_mode=MercahantModeModel()
        merchant_mode.merchant_id=self.merchant_id
        merchant_mode.bank_partner_id=self.bank_partner_id
        merchant_mode.mode_id=self.mode_id
        merchant_mode.save()
    @staticmethod
    def fetch_by_id(id):
        try:
            record=MercahantModeModel.objects.get(id=id)
            if record==None:
                return None
            return record
        except Exception as e:
            return None
    @staticmethod
    def fetch_by_merchant_id(merchant_id):
        record=MercahantModeModel.objects.filter(merchant_id=merchant_id)
        return record
    @staticmethod
    def fetch_by_merchant_id_and_mode(merchant_id,mode_id):
        record=MercahantModeModel.objects.filter(merchant_id=merchant_id,mode_id=mode_id,status=True)
        return record
    @staticmethod
    def fetchModesByMerchantId(merchant_id):
        cursors = connection.cursor()
        cursors.execute("select apis_mercahantmodemodel.status,apis_modemodel.mode, apis_modemodel.id from apis_modemodel inner join apis_mercahantmodemodel on apis_modemodel.id = apis_mercahantmodemodel.mode_id where apis_mercahantmodemodel.merchant_id="+merchant_id+";")
        # print("data ",(cursors.fetchall()))
        columns = [col[0] for col in cursors.description]
        print(columns)
        resp = [dict(zip(columns, row))
        for row in cursors.fetchall()
        ]
        return resp
    @staticmethod
    def deleteMerchantMode(merchant_id,admin_id,mode_id,bank_partner_id,status=None):
        merchantModeModel = MercahantModeModel()
        merchantModeModel = MercahantModeModel.objects.filter(merchant_id=merchant_id,mode_id=mode_id,bank_partner_id=bank_partner_id)
        if(len(merchantModeModel)==0):
            return -1
        try:
            merchantModeModel = MercahantModeModel.objects.filter(merchant_id=merchant_id,mode_id=mode_id,bank_partner_id=bank_partner_id).update(status=status,updated_by="admin ID :: "+str(admin_id),updated_at=datetime.now())
            print(merchantModeModel)
        except MercahantModeModel.DoesNotExist:
            return 0
        return 1
        