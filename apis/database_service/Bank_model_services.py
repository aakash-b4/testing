from django.db import connection
from ..models import BankPartnerModel as BankModel
from . import Log_model_services
from .. import const
class Bank_model_services:
    def __init__(self,bank_name=None,bank_code=None,nodal_account_number=None,nodal_ifsc=None,nodal_account_name=None):
        self.bank_name=bank_name
        self.bank_code=bank_code
        self.nodal_account_number=nodal_account_number
        self.nodal_ifsc=nodal_ifsc
        self.nodal_account_name=nodal_account_name
    def save(self,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="create",table_name="apis_bankpartnermodel",remarks="saving records in api_bankpartnermodel table",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        bankModel=BankModel()
        bankModel.bank_name=self.bank_name
        bankModel.bank_code=self.bank_code
        bankModel.nodal_account_number=self.nodal_account_number
        bankModel.nodal_ifsc=self.nodal_ifsc
        bankModel.nodal_account_name=self.nodal_account_name
        
        bankModel.save()
        log_service.table_id=bankModel.id
        log_service.save()
        return True
    @staticmethod
    def fetch_by_bankcode(bank_code,client_ip_address,created_by)->BankModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_bankpartnermodel",remarks="fetching records from apis_bankpartnermodel by bank code",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        bankModel=BankModel.objects.filter(bank_code=bank_code)
        log_service.save()
        if len(bankModel)==0:
            return None
        return bankModel[0]
    @staticmethod
    def fetch_by_id(id,client_ip_address,created_by)->BankModel:
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_bankpartnermodel",remarks="fetching records from apis_bankpartnermodel by primary key in the record",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        bankModel=BankModel.objects.get(id=id)
        log_service.table_id=bankModel.id
        log_service.save()
        return bankModel
    @staticmethod
    def ChargeBankInfo(bank_name,payoutMode,page,length,start,end):
        try:
            cursors = connection.cursor()
            cursors.execute("call chargeBreakUpInfo();")
            page = int(page)
            length=int(length)
            temp_bank_name="'"+bank_name+"'"
            temp_payout_mode="'"+payoutMode+"'"
            start_date = "'"+str(start)+"'"
            end_date = "'"+str(end)+"'"
            if(bank_name=="all"):
                temp_bank_name = "bank_name"
            if(payoutMode =="all"):
                temp_payout_mode = "mode"
            if(start=="all"):
                start_date="transaction_date"
            if(end=="all"):
                end_date="transaction_date"
            
            cursors.execute("select * from chargeInfoBankMode where bank_name = "+temp_bank_name+" and mode = "+temp_payout_mode+" and transaction_date>= "+start_date+" and transaction_date <= "+end_date+" limit "+str((page-1)*length)+","+str(length)+"")
            columns = [col[0] for col in cursors.description]
            
            resp = [
            dict(zip(columns, row))
            for row in cursors.fetchall()
            ]
            if(len(resp)==0):
                return -1
            cursors.execute("select sum(bank_charge) as sum_bank_charges,sum(bank_tax) as sum_bank_tax, sum(bank_total_charge) as sum_bank_total_charge from chargeInfoBankMode where bank_name = "+temp_bank_name+" and mode = "+temp_payout_mode+" and transaction_date>= "+start_date+" and transaction_date <= "+end_date+" limit "+str((page-1)*length)+","+str(length)+"")

            columns = [col[0] for col in cursors.description]
            total_charges =  [
            dict(zip(columns, row))
            for row in cursors.fetchall()
            ]

            cursors.execute("select sum(sabpaisa_charge) as sum_sabpaisa_charge,sum(sabpaisa_tax) as sum_sabpaisa_tax, sum(sabpaisa_total_charge) as sum_ssabpaisa_total_charge from chargeInfoBankMode where bank_name = "+temp_bank_name+" and mode = "+temp_payout_mode+" and transaction_date>= "+start_date+" and transaction_date <= "+end_date+" limit "+str((page-1)*length)+","+str(length)+"")        
            columns = [col[0] for col in cursors.description]
            
            total_sabpaisa = [
            dict(zip(columns, row))
            for row in cursors.fetchall()
            ]

            return {
                "Grid_data":resp,
                "total_charges_by_bank":total_charges,
                "total_charges_by_sabpaisa":total_sabpaisa
            }
        finally:
            cursors.execute("call deleteChargeBreakUpInfo();")