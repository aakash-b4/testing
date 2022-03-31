from datetime import date, datetime

from rest_framework import status
from ..models import ChargeModel,ModeModel
from . import Log_model_services
from .. import const

class charge_model_service:
    def __init__(self,mode=None,min_amount=None,max_amount=None,charge_percentage_or_fix=None,charge=None,created_at=None,deleted_at=None,updated_at=None,merchant_id=None,charge_type=None,partner_id=None):
        self.min_amount=min_amount
        self.max_amount=max_amount
        self.charge_percentage_or_fix=charge_percentage_or_fix
        self.charge = charge
        self.created_at = created_at
        self.deleted_at=deleted_at
        self.updated_at = updated_at
        self.merchant_id = merchant_id
        self.mode=mode
        self.charge_type=charge_type
        self.partner_id = partner_id
    def save(self,client_ip_address):
        log_service=Log_model_services.Log_Model_Service(log_type="create",table_name="apis_chargemodel",remarks="saving records in apis_chargemodel table",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by="mechant id :: "+self.merchant_id)
        chargeModel = ChargeModel()
        chargeModel.min_amount = self.min_amount
        chargeModel.max_amount = self.max_amount
        chargeModel.charge_percentage_or_fix = self.charge_percentage_or_fix
        chargeModel.charge = self.charge
        chargeModel.created_at = datetime.now()
       
        chargeModel.merchant_id= self.merchant_id
        modeid = ModeModel.objects.filter(mode=self.mode)
        chargeModel.mode_id=modeid[0].id
        chargeModel.created_at = datetime.now()
        chargeModel.partner_id=self.partner_id
        chargeModel.charge_type = self.charge_type
        # resp = ChargeModel.objects.get(mode_id=modeid,min_amount=self.min_amount,max_amount=self.max_amount,
        # charge_percentage_or_fix=self.charge_percentage_or_fix,charge=self.charge,partner_id=self.partner_id,charge_type=self.charge_type)
        # print(resp)
        chargeModel.save()
        log_service.table_id=chargeModel.id

        log_service.save()
        return chargeModel.id
    @staticmethod
    def fetch_by_id(client_ip_address,created_by,page,length,merchant_id=None):
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_chargemodel",remarks="fetching records from apis_chargemodel by primary key in the record",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        offSet = (int(page)-1)*int(length)
        print("select * from apis_chargemodel where merchant_id = "+merchant_id+" order by id desc limit "+str(offSet) +" "+str(length)+";")
        chargeModel=ChargeModel.objects.raw("select * from apis_chargemodel where merchant_id = "+merchant_id+" and status = true order by id desc limit "+str(offSet) +","+str(length)+";")
        resp=list()

        for data in list(chargeModel.iterator()):
            mode=ModeModel.objects.get(id=data.mode_id)
            d={
                "id": data.id,
                "mode_id": data.mode_id,
                "mode_name":mode.mode,
                "min_amount": data.min_amount,
                "max_amount": data.max_amount,
                "charge_percentage_or_fix": data.charge_percentage_or_fix,
                "charge": data.charge,
                "merchant_id": data.merchant_id
            }
            resp.append(d)
        log_service.save()
        return resp

    def allCharges(client_ip_address,created_by,page,length,merchant_id=None):
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_chargemodel",remarks="fetching records from apis_chargemodel by primary key in the record",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        offSet = (int(page)-1)*int(length)
        chargeModel=ChargeModel.objects.raw("select * from apis_chargemodel where status=true order by id desc limit "+str(offSet) +","+str(length)+";")
        resp=list()
        for data in list(chargeModel.iterator()):
            d={
                "id": data.id,
                "mode_id": data.mode_id,
                "min_amount": data.min_amount,
                "max_amount": data.max_amount,
                "charge_percentage_or_fix": data.charge_percentage_or_fix,
                "charge": data.charge,
                "merchant_id": data.merchant_id
            }
            resp.append(d)
        log_service.save()
        return resp

    def deleteCharge(id):
        resp = ChargeModel.objects.filter(id=id)
        if(resp==None):
            return -1
        resp = ChargeModel.objects.filter(id=id).update(status=False,deleted_at=datetime.now())
        return 1
    
    def updateCharge(id,min_amount,max_amount):
        obj = ChargeModel.objects.get(id=id,status=True)
        oldCharge=ChargeModel()

        oldCharge.min_amount = obj.min_amount
        oldCharge.max_amount = obj.max_amount
        oldCharge.charge_percentage_or_fix = obj.charge_percentage_or_fix
        oldCharge.charge = obj.charge
        oldCharge.created_at = datetime.now()
        oldCharge.merchant_id= obj.merchant_id
        print("yo======== ",oldCharge.mode_id)
        modeid = ModeModel.objects.filter(mode=obj.mode)
        oldCharge.mode_id=modeid[0].id
        oldCharge.created_at = datetime.now()
        oldCharge.partner_id=obj.partner_id
        oldCharge.charge_type = obj.charge_type
        oldCharge.status=False
        oldCharge.save()
        resp=ChargeModel.objects.filter(id=id).update(min_amount=min_amount,max_amount=max_amount,updated_at=datetime.now())
        return 1
