from apis.database_models.BankModel import BankPartnerModel
from apis.database_models.ModeModel import ModeModel
from apis.view_api import bankpartner
from apis.database_models.ClientModel import MerchantModel
from datetime import date, datetime
from rest_framework import status
from ..database_models.MerchantModeModel import MercahantModeModel
from ..database_service.Log_model_services import Log_Model_Service
from .. import const

class Merchant_mode_service:
    def __init__(self,merchant_id=None,bank_partner_id=None,mode_id=None):
        self.merchant_id=merchant_id
        self.bank_partner_id = bank_partner_id
        self.mode_id=mode_id

    def save(self,admin_id):
        resp = MercahantModeModel.objects.filter(merchant_id=self.merchant_id,mode_id=self.mode_id,bank_partner_id=self.bank_partner_id)
        if(len(resp)!=0):
            return 0
        merchantModeModel = MercahantModeModel()
        merchantModeModel.merchant_id = self.merchant_id
        merchantModeModel.bank_partner_id= self.bank_partner_id
        merchantModeModel.mode_id = self.mode_id
        merchantModeModel.status = True
        merchantModeModel.created_by = "admin id :: "+admin_id
        merchantModeModel.save()
        return 1
    @staticmethod
    def fetchAllMerchantModes():
        merchantModeModel = MercahantModeModel.objects.filter(status=True).all().values()
        if(len(merchantModeModel)==0):
            return 0
        resp = list()
        
        for data in merchantModeModel:
            merchant=MerchantModel.objects.filter(id=data.get("merchant_id")).values()
            print("merchant ------ ",str(merchant[0].get("client_username")))
            bank = BankPartnerModel.objects.filter(id=data.get("bank_partner_id")).values()
            print("bank ----- ",str(bank))
            mode = ModeModel.objects.filter(id= data.get("mode_id")).values()
            print("mode ------- ",str(mode))
            d={
                "merchant_id":data.get("merchant_id"),
                "merchant_client_username":merchant[0].get("client_username"),
                "merchant_client_name":merchant[0].get("client_name"),
                "bank_partner_id":data.get("bank_partner_id"),
                "bank_name":bank[0].get("bank_name"),
                "bank_code":bank[0].get("bank_code"),
                "mode_id":data.get("mode_id"),
                "mode_name":mode[0].get("mode"),
                "status":data.get("status")
            }
            resp.append(d)
        return resp
    @staticmethod
    def fetchMerchantModeById(merchant_id):
        merchantModeModel = MercahantModeModel.objects.filter(merchant_id=merchant_id,status=True).all().values()
        if(len(merchantModeModel)==0):
            return 0
        resp = list()
        for data in merchantModeModel:
            merchant=MerchantModel.objects.filter(id=data.get("merchant_id")).values()
            print("merchant ------ ",str(merchant[0].get("client_username")))
            bank = BankPartnerModel.objects.filter(id=data.get("bank_partner_id")).values()
            print("bank ----- ",str(bank))
            mode = ModeModel.objects.filter(id= data.get("mode_id")).values()
            print("mode ------- ",str(mode))
            d={
                "merchant_id":data.get("merchant_id"),
                "merchant_client_username":merchant[0].get("client_username"),
                "merchant_client_name":merchant[0].get("client_name"),
                "bank_partner_id":data.get("bank_partner_id"),
                "bank_name":bank[0].get("bank_name"),
                "bank_code":bank[0].get("bank_code"),
                "mode_id":data.get("mode_id"),
                "mode_name":mode[0].get("mode"),
                "status":data.get("status")
            }
            resp.append(d)
        return resp
    # @staticmethod
    # def deleteMerchantMode(merchant_id,admin_id,mode_id,bank_partner_id):
    #     merchantModeModel = MercahantModeModel()
    #     try:
    #         merchantModeModel = MercahantModeModel.objects.filter(merchant_id=merchant_id,status=True,mode_id=mode_id,bank_partner_id=bank_partner_id)
    #     except MercahantModeModel.DoesNotExist:
    #         return 0
    #     print("merchant model "+str(len(merchantModeModel))+"    "+str(merchantModeModel))
    #     merchantModeModel[0].status = False
    #     merchantModeModel[0].deleted_by = "admin ID :: "+str(admin_id)
    #     merchantModeModel[0].deleted_at = datetime.now()
    #     merchantModeModel[0].save()
    #     return 1
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
        
        