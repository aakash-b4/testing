from ..database_service.Client_model_service import Client_Model_Service
from ..database_service.Ledger_model_services import Ledger_Model_Service
class Ledger_service:
    def __init__(self,merchant_id,client_ip_address,created_by):
        self.merchant_id=merchant_id
        self.client_ip_address=client_ip_address
        self.created_by=created_by
    def getLedgerForMerchant(self):
        client_model=Client_Model_Service.fetch_by_id(self.merchant_id,self.client_ip_address,self.created_by)
        json={}
        json["username"]=client_model.client_username
        json["id"]=client_model.id
        json['email']=client_model.email
        json['is_ip_checking']=client_model.is_ip_checking
        json['phone_number']=client_model.phone
        json['balance']=Ledger_Model_Service.getBalance(self.merchant_id,self.client_ip_address,self.created_by)
        json['credited']=Ledger_Model_Service.getCreditedAmount(self.merchant_id,self.client_ip_address,self.created_by)
        json["debited"]=Ledger_Model_Service.getDebitedAmount(self.merchant_id,self.client_ip_address,self.created_by)
        return json