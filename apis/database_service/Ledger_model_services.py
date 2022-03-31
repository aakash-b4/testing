from typing import Text

from django.views.generic import base
from apis.database_models.ClientModel import MerchantModel
from ..database_service.Charge_breaking_model_services import Charge_Breaking_model_services
from requests.api import request
from apis import const
from apis.Utils import *
import string
import random
from rest_framework import status
from sabpaisa import auth
from datetime import date, datetime
from apis.Utils.generater import *
from ..Utils import statuscodes
from ..database_service import Client_model_service
from rest_framework.permissions import AND
from ..models import TransactionHistoryModel as LedgerModel
from ..models import ModeModel
from ..Utils.numbers import get_number

from ..models import ChargeModel
from ..database_models.VariableModel import VariableModel
from ..database_models.ChargeBreakingModel import ChargeBreakingModel
from . import Log_model_services
from ..Utils import formulas
from django.db import connection
from sabpaisa import main
from ..database_models.TaxModel import TaxModel
import pytz

from apis import Utils


class Ledger_Model_Service:
    def __init__(self, id=None, purpose=None, total_amount=None, is_tax_inclusive=None, upiId=None, status_code=None,
                 tax=None, merchant=None, charge_id=None, client_code=None, linked_ledger_id=None, payout_trans_id=None,
                 trans_amount_type=None, type_status=None, amount=None, van=None, trans_type=None, trans_status=None,
                 bank_ref_no=None, customer_ref_no=None, bank_id=None, trans_time=None, bene_account_name=None,
                 bene_account_number=None, bene_ifsc=None, request_header=None, createdBy=None, updatedBy=None,
                 deletedBy=None, created_at=None, deleted_at=None, updated_at=None, status=True, mode=None,
                 charge=None):
        self.id = id
        self.merchant = merchant
        self.client_code = client_code
        self.amount = amount
        self.purpose = purpose
        self.trans_type = trans_type
        self.trans_status = trans_status
        self.is_tax_inclusive = is_tax_inclusive
        self.bank_ref_no = bank_ref_no
        self.customer_ref_no = customer_ref_no
        self.trans_amount_type = trans_amount_type
        self.bank_id = bank_id
        self.trans_time = trans_time
        self.linked_ledger_id = linked_ledger_id
        self.type_status = type_status
        self.bene_account_name = bene_account_name
        self.bene_account_number = bene_account_number
        self.bene_ifsc = bene_ifsc
        self.payout_trans_id = payout_trans_id
        self.charge_id = charge_id
        self.status_code = status_code
        self.upiId = upiId
        self.request_header = request_header
        self.van = van
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        self.deletedBy = deletedBy
        self.tax = tax
        self.total_amount = total_amount
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.updated_at = updated_at
        # self.status = status
        self.mode = mode
        self.charge = charge

    def to_json(self):
        json = {}
        json["amount"] = self.amount
        json['customer_ref_no'] = self.customer_ref_no
        json["trans_time"] = str(self.trans_time)
        json['payout_trans_id'] = self.payout_trans_id
        json['charge'] = self.charge
        json['mode'] = self.mode
        json["bene_account_name"] = self.bene_account_name
        json['bene_account_number'] = self.bene_account_number
        json['bene_ifsc'] = self.bene_ifsc
        json["trans_status"] = self.trans_status
        return json

    def save(self, createdBy, client_ip_address=None):
        # log_service = Log_model_services.Log_Model_Service(log_type="create",table_name="apis_ledgermodel",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        ledgermodel = LedgerModel()
        ledgermodel.merchant_id = self.merchant
        ledgermodel.client_code = self.client_code
        ledgermodel.amount = self.amount
        ledgermodel.trans_type = self.trans_type
        ledgermodel.type_status = self.type_status
        ledgermodel.trans_status = self.trans_status
        ledgermodel.created_at = datetime.now()
        ledgermodel.bank_ref_no = self.bank_ref_no
        ledgermodel.customer_ref_no = self.customer_ref_no
        ledgermodel.bank_partner_id = self.bank_id
        ledgermodel.total_amount = self.total_amount
        ledgermodel.trans_init_time = self.trans_time
        ledgermodel.payout_trans_id = self.payout_trans_id
        ledgermodel.trans_date = date.today()
        ledgermodel.trans_amount_type = self.trans_amount_type
        ledgermodel.van = self.van
        if self.bene_account_name != None:
            ledgermodel.bene_account_name = self.bene_account_name
        if self.bene_account_number != None:
            ledgermodel.bene_account_number = self.bene_account_number
        if self.bene_ifsc != None:
            ledgermodel.bene_ifsc = self.bene_ifsc
        ledgermodel.request_header = self.request_header
        ledgermodel.purpose = self.purpose
        ledgermodel.createdBy = self.createdBy
        ledgermodel.updatedBy = self.updatedBy
        ledgermodel.tax = self.tax
        ledgermodel.is_tax_inclusive = self.is_tax_inclusive
        ledgermodel.linked_Txn_id = self.linked_ledger_id
        ledgermodel.deletedBy = self.deletedBy
        # ledgermodel.created_at = self.created_at
        ledgermodel.deleted_at = self.deleted_at
        ledgermodel.updated_at = self.updated_at
        # ledgermodel.status = self.status
        ledgermodel.status_code = self.status_code
        ledgermodel.payment_mode_id = self.mode
        ledgermodel.charge = self.charge
        if self.charge_id != None:
            ledgermodel.charge_id = self.charge_id
        if self.upiId != None:
            ledgermodel.upi_id = self.upiId
        ledgermodel.save()

        # start
        # clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
        #     id=self.merchant, created_by=createdBy, client_ip_address=client_ip_address)

        # authKey = clientModel.auth_key
        # authIV = clientModel.auth_iv
        # respId = ledgermodel.id
        # if(ledgermodel.id<=0):
        #     return "0"
        # resp = str(respId)
        # encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        # return encResp
        return ledgermodel.id
        # end

    @staticmethod
    def calculate_tax(is_inclusive, charges):
        tax = 0
        taxmodel = TaxModel.objects.filter(status=True)
        ls = []
        total_charge = 0
        for i in charges:

            if is_inclusive:
                base = formulas.calulate_base(i[0], taxmodel[0].tax)
                tax_temp = i[0] - base
                i[0] = base
                tax = tax + tax_temp
                total_charge += base
                ls.append([i[1].id, tax_temp, base])
            else:
                tax_temp = formulas.calulate_tax_exclusive(i[0], taxmodel[0].tax)
                tax = tax + tax_temp
                total_charge += i[0]
                ls.append([i[1].id, tax_temp, i[1].charge])
        return [tax, ls, total_charge]

    @staticmethod
    def fetch_by_customer_ref_no(merchant_id, customer_ref):
        ledger = LedgerModel.objects.filter(merchant_id=merchant_id, customer_ref_no=customer_ref)
        if len(ledger) > 0:
            return None
        return ledger

    def fetch_by_clientid(self, client_id, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel",
                                                           remarks="fetching all records from ledger table by client id",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)
        ledgerModels = LedgerModel.objects.filter(client_id=client_id)
        log_service.save()
        return ledgerModels

    def fetch_by_clientcode(self, client_code, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel",
                                                           remarks="fetching all records from ledger table by client code ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModels = LedgerModel.objects.filter(client_code=client_code)
        log_service.save()
        return ledgerModels

    @staticmethod
    def fetch_by_id(id, client_ip_address, created_by) -> LedgerModel:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel",
                                                           remarks="fetching record from ledger table by primary key ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModels = LedgerModel.objects.get(id=id)
        log_service.table_id = ledgerModels.id
        log_service.save()
        return ledgerModels

    @staticmethod
    def fetch_by_linked_id(id):
        ledgerModels = LedgerModel.objects.filter(linked_Txn_id=id)
        if len(ledgerModels) == 0:
            return None
        return ledgerModels

    @staticmethod
    def fetch_by_id_tojson(id, client_ip_address, created_by) -> LedgerModel:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel",
                                                           remarks="fetching record from ledger table by primary key ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModels = LedgerModel.objects.get(id=id)
        json = {}
        json["orderId"] = str(ledgerModels.customer_ref_no)
        json['amount'] = str(ledgerModels.amount)
        json['status'] = str(ledgerModels.trans_status)
        json['payoutTransactionId'] = str(ledgerModels.payout_trans_id)
        json['bankRefNo'] = str(ledgerModels.bank_ref_no)
        json['transactionCompletionDate'] = str(ledgerModels.trans_completed_time)
        log_service.table_id = ledgerModels.id
        log_service.save()
        return json

    def fetch_by_van(self, van, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel",
                                                           remarks="fetching all records from ledger table by van ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModels = LedgerModel.objects.filter(van=van)
        log_service.save()
        return ledgerModels

    @staticmethod
    def fetch_customer_ref_no(merchant, customer_ref_no, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel",
                                                           remarks="fetching all records from ledger table by van ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)
        ledger_models = LedgerModel.objects.filter(merchant_id=merchant, customer_ref_no=customer_ref_no,
                                                   trans_type="payout")

        print("query : ", ledger_models.query)
        log_service.save()
        return ledger_models

    def update_status(self, id, status, client_ip_address, created_by, utr="null"):
        log_service = Log_model_services.Log_Model_Service(log_type="update", table_name="apis_ledgermodel",
                                                           remarks="updating status from ledger table for the record fetched by id ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModel = LedgerModel.objects.get(id=id)
        ledgerModel.trans_status = status
        ledgerModel.bank_ref_no = utr
        ledgerModel.status_code = statuscodes.statuscodes[status]
        ledgerModel.updated_at = datetime.now()
        ledgerModel.save()
        log_service.table_id = ledgerModel.id

        log_service.save()
        return ledgerModel

    def update_upi_icici_status(self, id, status, client_ip_address, created_by, remarks, system_remarks,
                                bene_account_number,
                                UserProfile, SeqNo, MobileAppData, PayerRespCode, bank_ref_no="null"):
        log_service = Log_model_services.Log_Model_Service(log_type="update", table_name="apis_ledgermodel",
                                                           remarks="updating icici status from ledger table for the record fetched by id ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModel = LedgerModel.objects.get(id=id)
        ledgerModel.trans_status = status
        ledgerModel.bank_ref_no = bank_ref_no
        ledgerModel.status_code = statuscodes.statuscodes[status]
        ledgerModel.system_remarks = system_remarks
        ledgerModel.remarks = remarks
        ledgerModel.bene_account_number = bene_account_number
        ledgerModel.seq_no = SeqNo
        ledgerModel.user_profile = UserProfile
        ledgerModel.mobile_app_data = MobileAppData
        ledgerModel.payer_resp_code = PayerRespCode
        ledgerModel.updated_at = datetime.now()
        ledgerModel.save()
        log_service.table_id = ledgerModel.id

        log_service.save()
        return ledgerModel

    def update_neft_rtgs_icici_status(self, id, status, client_ip_address, created_by, utr, urn, uniqueId, response):
        log_service = Log_model_services.Log_Model_Service(log_type="update", table_name="apis_ledgermodel",
                                                           remarks="updating icici status from ledger table for the record fetched by id ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModel = LedgerModel.objects.get(id=id)
        ledgerModel.trans_status = status
        ledgerModel.status_code = statuscodes.statuscodes[status]
        ledgerModel.system_remarks = response
        ledgerModel.user_profile = urn
        ledgerModel.mobile_app_data = uniqueId
        ledgerModel.payer_resp_code = utr
        ledgerModel.updated_at = datetime.now()
        ledgerModel.save()
        log_service.table_id = ledgerModel.id

        log_service.save()
        return ledgerModel

    def update_imps_icici_status(self, id, status, client_ip_address, created_by, remarks, system_remarks,
                                 bene_account_number,
                                 UserProfile, SeqNo, MobileAppData, PayerRespCode, TranDateTime, RemName, RetailerCode,
                                 bank_ref_no="null"):
        log_service = Log_model_services.Log_Model_Service(log_type="update", table_name="apis_ledgermodel",
                                                           remarks="updating icici status from ledger table for the record fetched by id ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModel = LedgerModel.objects.get(id=id)
        ledgerModel.trans_status = status
        ledgerModel.trans_date_time = TranDateTime
        ledgerModel.remitter_name = RemName
        ledgerModel.retailer_code = RetailerCode
        ledgerModel.bank_ref_no = bank_ref_no
        ledgerModel.status_code = statuscodes.statuscodes[status]
        ledgerModel.system_remarks = system_remarks
        ledgerModel.remarks = remarks
        ledgerModel.bene_account_number = bene_account_number
        ledgerModel.seq_no = SeqNo
        ledgerModel.user_profile = UserProfile
        ledgerModel.mobile_app_data = MobileAppData
        ledgerModel.payer_resp_code = PayerRespCode
        ledgerModel.updated_at = datetime.now()
        ledgerModel.save()
        log_service.table_id = ledgerModel.id

        log_service.save()
        return ledgerModel

    def update_trans_time(self, id, completion_time, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="update", table_name="apis_ledgermodel",
                                                           remarks="updating status from ledger table for the record fetched by id ",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        ledgerModel = LedgerModel.objects.get(id=id)
        ledgerModel.trans_completed_time = datetime.now()
        ledgerModel.updated_at = datetime.now()
        ledgerModel.save()
        log_service.table_id = ledgerModel.id

        log_service.save()
        return ledgerModel

    def deleteById(id, deletedBy, merchant, client_ip_address, createdBy):
        log_service = Log_model_services.Log_Model_Service(log_type="delete", table_name="apis_ledgermodel",
                                                           remarks="deleting records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=createdBy)
        ledger = LedgerModel.objects.filter(id=id, merchant_id=merchant)
        if (len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]

            ledgerModel.status = False
            ledgerModel.deletedBy = deletedBy
            ledgerModel.deleted_at = datetime.now()
            ledgerModel.save()
            log_service.table_id = id
            log_service.save()
            return True
        return False

    # def fetchAll(self):
    #     ledgerModel = LedgerModel.objects.filter(status=True)
    #     return ledgerModel
    def deleteLedger(self, id):
        LedgerModel.objects.filter(id=id).delete()
        return True

    @staticmethod
    def getBalance(merchant_id, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="get balance", table_name="apis_ledgermodel",
                                                           remarks="getting balance from apis_ledgermodel table via getBalance stored procedure",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        cursors = connection.cursor()
        print(merchant_id)
        rec = VariableModel.objects.filter(variable_name="getBalance")
        if len(rec) == 0 or rec[0].variable_value == "first":
            cursors.execute("call getBalance('" + merchant_id + "',@balance,@cred,@deb)")
        else:
            cursors.execute("call getBalancenew('" + merchant_id + "',@balance,@cred,@deb)")
        cursors.execute("select @balance")
        # cursors.execute("Call getAmount("'credited'",5,@cred);")
        # cursors.execute("Call getAmount("'debited'",5,@deb);")
        # cursors.execute("")
        value = cursors.fetchall()
        cursors.close()
        print(value[0][0])
        log_service.save()
        return float(value[0][0])

    @staticmethod
    def getDebitedAmount(merchant_id, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="get Debited Amount",
                                                           table_name="apis_transaction_history",
                                                           remarks="getting transaction_history from getAmount stored procedure",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        cursors = connection.cursor()

        cursors.execute('Call getAmount("dr",' + merchant_id + ',@deb)')
        cursors.execute('select @deb')

        # cursors.execute("select @balance")
        # cursors.execute("Call getAmount("'credited'",5,@cred);")
        # cursors.execute("Call getAmount("'debited'",5,@deb);")
        # cursors.execute("")
        # columns = [col[0] for col in cursors.description]
        # print(columns)
        return cursors.fetchall()[0][0]

    @staticmethod
    def getCreditedAmount(merchant_id, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="get Debited Amount",
                                                           table_name="apis_transaction_history",
                                                           remarks="getting transaction_history from getAmount stored procedure",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        cursors = connection.cursor()

        cursors.execute('Call getAmount("cr",' + merchant_id + ',@cred)')
        cursors.execute('select @cred')

        # cursors.execute("select @balance")
        # cursors.execute("Call getAmount("'credited'",5,@cred);")
        # cursors.execute("Call getAmount("'debited'",5,@deb);")
        # cursors.execute("")
        # columns = [col[0] for col in cursors.description]
        # print(columns)

        # dict(zip(columns, row))
        return cursors.fetchall()[0][0]

    @staticmethod
    def getTransactionHistory(page, length, start, end, merchant_id, transfer_type, trans_status):
        try:
            page = int(page)
            length = int(length)
            transfer_type_temp = "'" + transfer_type + "'"
            trans_status_temp = "'" + trans_status + "'"

            if transfer_type == "all":
                transfer_type_temp = "trans_type"

            if trans_status == "all":
                trans_status_temp = "trans_status"
            cursors = connection.cursor()

            if start == "all":
                start = "created_at"
                tempstart = "apis_transactionhistorymodel.created_at"
            else:
                start = "'" + str(start) + "'"
                tempstart = start
            if end == "all":
                end = "created_at"
                tempend = "apis_transactionhistorymodel.created_at"
            else:
                end = "'" + str(end) + "'"
                tempend = end

            # if start=="all" and end=="all":
            # print("if")
            # print("select apis_transactionhistorymodel.*,apis_merchantmodel.client_username,apis_merchantmodel.client_name from apis_transactionhistorymodel inner join apis_merchantmodel on apis_transactionhistorymodel.merchant_id=apis_merchantmodel.id where  merchant_id="+str(merchant_id)+" and trans_type="+transfer_type_temp+" and trans_status="+trans_status_temp+" order by apis_transactionhistorymodel.id desc limit "+str((page-1)*length)+","+str(length)+"")
            # record=LedgerModel.objects.raw("select apis_transactionhistorymodel.*,apis_merchantmodel.client_username,apis_merchantmodel.client_name from apis_transactionhistorymodel inner join apis_merchantmodel on apis_transactionhistorymodel.merchant_id=apis_merchantmodel.id where  merchant_id="+str(merchant_id)+" and trans_type="+transfer_type_temp+" and trans_status="+trans_status_temp+" order by apis_transactionhistorymodel.id desc limit "+str((page-1)*length)+","+str(length)+"")
            # # print(list(record.iterator()))
            # print(record.columns)

            # cursors.execute("select sum(total_amount) as credit from apis_transactionhistorymodel where  merchant_id="+str(merchant_id)+" and trans_amount_type='cr' and trans_status in ('Success')")
            # credit_temp= cursors.fetchall()[0][0]
            # # credit_amount=LedgerModel.objects.raw("select sum(total_amount) as credit from apis_transactionhistorymodel where  merchant_id="+str(merchant_id)+" and trans_amount_type='cr' and trans_status in ('Success')")
            # # debit_amount=LedgerModel.objects.raw("select sum(total_amount) as debit from apis_transactionhistorymodel where  merchant_id="+str(merchant_id)+" and trans_amount_type='dr' and trans_status in ('Success','Requested','Pending','Initiated')")
            # # print(list(credit_amount.iterator()))
            # cursors.execute("select sum(total_amount) as debit from apis_transactionhistorymodel where  merchant_id="+str(merchant_id)+" and trans_amount_type='dr' and trans_status in ('Success','Requested','Pending','Initiated')")
            # debit_temp=cursors.fetchall()[0][0]
            # if credit_temp==None:
            #     credit_temp=0
            # if debit_temp==None:
            #     debit_temp=0

            # balance=credit_temp-debit_temp
            # total_s=cursors.execute("select count(*) as total_rec from apis_transactionhistorymodel where  merchant_id="+str(merchant_id)+" and trans_type='payout' and trans_status="+trans_status_temp)
            # temp_total=cursors.fetchall()[0][0]
            # cursors.execute("select count(*) from apis_transactionhistorymodel where  merchant_id="+str(merchant_id)+" ")
            # total_trans=cursors.fetchall()[0][0]
            # record=LedgerModel.objects.filter(merchant=merchant_id)
            # print("record :: ",record)

            # else:
            print(
                "select apis_transactionhistorymodel.*,apis_merchantmodel.client_username from apis_transactionhistorymodel inner join apis_merchantmodel on apis_transactionhistorymodel.merchant_id=apis_merchantmodel.id where  merchant_id=" + str(
                    merchant_id) + " and  apis_transactionhistorymodel.created_at between " + str(
                    tempstart) + " and " + str(tempend) + " order by apis_transactionhistorymodel.id desc limit " + str(
                    length) + " offset " + str((page - 1) * length) + "")
            record = LedgerModel.objects.raw(
                "select apis_transactionhistorymodel.*,apis_merchantmodel.client_username,apis_merchantmodel.client_name from apis_transactionhistorymodel inner join apis_merchantmodel on apis_transactionhistorymodel.merchant_id=apis_merchantmodel.id where  merchant_id=" + str(
                    merchant_id) + " and trans_type=" + transfer_type_temp + " and trans_status=" + trans_status_temp + " and  apis_transactionhistorymodel.created_at between " + str(
                    tempstart) + " and " + str(tempend) + " order by apis_transactionhistorymodel.id desc limit " + str(
                    length) + " offset " + str((page - 1) * length) + "")
            cursors.execute(
                "select sum(total_amount) as credit from apis_transactionhistorymodel where  merchant_id=" + str(
                    merchant_id) + " and trans_amount_type='cr' and trans_status in ('Success') and created_at between " + str(
                    start) + " and " + str(end) + "")

            credit_temp = cursors.fetchall()[0][0]
            cursors.execute(
                "select sum(total_amount) as debit from apis_transactionhistorymodel where  merchant_id=" + str(
                    merchant_id) + " and trans_amount_type='dr' and trans_status in ('Success','Requested','Pending','Initiated') and created_at between " + str(
                    start) + " and " + str(end) + "")
            debit_temp = cursors.fetchall()[0][0]
            if credit_temp == None:
                credit_temp = 0
            if debit_temp == None:
                debit_temp = 0

            balance = credit_temp - debit_temp
            cursors.execute("select count(*) as total_rec from apis_transactionhistorymodel where  merchant_id=" + str(
                merchant_id) + " and trans_type='payout' and trans_status=" + trans_status_temp + " and created_at between " + str(
                start) + " and " + str(end) + "")
            temp_total = cursors.fetchall()[0][0]
            cursors.execute("select count(*) from apis_transactionhistorymodel where  merchant_id=" + str(
                merchant_id) + " and created_at between " + str(start) + " and " + str(end) + " ")
            total_trans = cursors.fetchall()[0][0]
            # print("record :: ",record)
            from . import Mode_model_services
            modes = Mode_model_services.Mode_Model_Service.fetch_all()
            mode_maps = {}
            for i in modes:
                mode_maps[i.id] = i.mode

            def rec(rec):

                json = {"customer_ref_no": rec.customer_ref_no, "trans_completed_time": rec.trans_completed_time,
                        "trans_init_time": rec.trans_init_time, "charge": rec.charge,
                        "payment_mode": mode_maps[rec.payment_mode_id], "bene_account_name": rec.bene_account_name,
                        "bene_account_number": rec.bene_account_number, "bene_ifsc": rec.bene_ifsc,
                        "payout_trans_id": rec.payout_trans_id, "tax_amount": rec.tax, "total_amount": rec.total_amount,
                        "created_at": rec.created_at, "updated_at": rec.updated_at, "deleted_at": rec.deleted_at,
                        "trans_amount_type": rec.trans_amount_type, "merchant_id": rec.merchant_id,
                        "client_username": rec.client_username, "client_name": rec.client_name, "id": rec.id,
                        "amount": rec.amount, "type_status": rec.type_status, "trans_type": rec.trans_type,
                        "trans_status": rec.trans_status, "upi_id": rec.upi_id,
                        "unique_transaction_ref": rec.bank_ref_no}
                return json

            data = list(map(rec, list(record.iterator())))
            return {"data": data, "balance": balance, "payout_rec": temp_total, "total_transactions": total_trans}
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return None

    @staticmethod
    def getLedgers(page, length, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="get ledgers",
                                                           table_name="apis_transaction_history",
                                                           remarks="getting ledgers from getLedgers stored procedure",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)

        cursors = connection.cursor()

        cursors.execute("call getLedger(" + length + "," + page + ")")
        # cursors.execute("select @balance")
        # cursors.execute("Call getAmount("'credited'",5,@cred);")
        # cursors.execute("Call getAmount("'debited'",5,@deb);")
        # cursors.execute("")
        columns = [col[0] for col in cursors.description]
        # print(columns)
        return [
            dict(zip(columns, row))
            for row in cursors.fetchall()
        ]
        # value = cursors.fetchall()

        # cursors.close()
        # print(value)
        # log_service.save()
        # return value        

    @staticmethod
    def calculate_charge(merchant_id, mode, amount, client_ip_address):

        mode = ModeModel.objects.filter(mode=mode)
        print(mode)
        print(mode[0].id)
        charge = ChargeModel.objects.filter(mode_id=mode[0].id, min_amount__lt=amount, max_amount__gt=amount,
                                            merchant_id=merchant_id, status=True)
        # print(charge[0].charge_percentage_or_fix)
        charge_amount = 0
        charge_list = []
        for i in charge:
            cc = get_number(i.charge_percentage_or_fix, amount, i.charge)
            charge_list.append([cc, i])
            charge_amount += cc
        if len(charge) == 0:
            return [0, 0]
        else:
            return [charge_amount, charge_list]
        # if(len(charge)>0 and charge[0].charge_percentage_or_fix=="percentage"):
        #     charge_amount=(amount/100)*charge[0].charge
        #     return charge_amount
        # elif (len(charge)>0 and charge[0].charge_percentage_or_fix=="fix"):
        #     print(charge[0].charge)
        #     return charge[0].charge
        # else:
        #     return 0

    def update(self, id, merchant, client_ip_address, created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="update", table_name="apis_ledgermodel",
                                                           remarks="updating records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)
        log_service.table_id = id
        log_service.save()
        ledger = LedgerModel.objects.filter(id=id, merchant_id=merchant)
        if (len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            ledgermodel.id = id
            ledgermodel.merchant_id = self.merchant
            ledgermodel.client_code = self.client_code
            ledgermodel.amount = self.amount
            ledgermodel.trans_type = self.trans_type
            ledgermodel.type_status = self.type_status
            ledgermodel.trans_status = self.trans_status
            ledgermodel.bank_ref_no = self.bank_ref_no
            ledgermodel.customer_ref_no = self.customer_ref_no
            ledgermodel.bank_partner_id = self.bank_id
            ledgermodel.trans_time = self.trans_time
            ledgermodel.van = self.van
            ledgermodel.bene_account_name = self.bene_account_name
            ledgermodel.bene_account_number = self.bene_account_number
            ledgermodel.bene_ifsc = self.bene_ifsc
            ledgermodel.request_header = self.request_header
            ledgermodel.createdBy = self.createdBy
            ledgermodel.updatedBy = self.updatedBy
            ledgermodel.deletedBy = self.deletedBy
            ledgermodel.updated_at = self.updated_at
            # ledgermodel.deleted_at = ledgermodel.deleted_at
            # ledgermodel.created_at = ledgermodel.created_at
            ledgermodel.created_at = self.created_at
            ledgermodel.status = self.status
            ledgermodel.payment_mode_id = self.mode
            ledgermodel.charge = self.charge
            ledgermodel.save()
        return ledgermodel.id

    # @staticmethod
    # def getBalance(clientCode):
    #     cursors = connection.cursor()
    #     cursors.execute('call getBalance("'+clientCode+'",@balance)')
    #     cursors.execute("select @balance")
    #     value = cursors.fetchall()
    #     cursors.close()

    #     print(value)
    #     return value[0][0]

    def updateTransTime(id, transTime):
        ledger = LedgerModel.objects.filter(id=id)
        print("service ledger = ", ledger)
        if (len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            print("service     ", ledgerModel)
            ledgerModel.updated_at = datetime.now()
            ledgerModel.trans_time = transTime
            ledgerModel.save()
            return True
        return False

    @staticmethod
    def addAmount(decResp, client_ip_address, admin, amount):
        log_service = Log_model_services.Log_Model_Service(json=str({"merchant_id": decResp.get("merchant_id")}),
                                                           log_type="create", table_name="apis_ledgermodel",
                                                           remarks="saving records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip,
                                                           created_by=decResp.get("created_by"))
        linkedId = generate_token()
        charge = Ledger_Model_Service.addCharge(decResp, client_ip_address, admin, amount, linkedId)

        ledgermodel = LedgerModel()
        ledgermodel.amount = amount
        modeOfTrans = decResp.get("mode")
        m = ModeModel.objects.filter(mode=modeOfTrans)
        ledgermodel.payment_mode_id = m[0].id
        ledgermodel.bank_ref_no = decResp.get("bank_ref_no")
        ledgermodel.trans_amount_type = "cr"
        ledgermodel.trans_type = "payin"
        ledgermodel.type_status = "Generated"
        ledgermodel.trans_date = date.today()
        ledgermodel.request_header = "request header"
        bankResp = "NULL"
        ledgermodel.purpose = "CREDIT"
        ledgermodel.remarks = decResp.get("remarks")
        ledgermodel.merchant_id = decResp.get("merchant_id")
        ledgermodel.client_code = "null"
        # CR06e65070-dbd6-11eb-9816-507b9d006cb8
        ledgermodel.customer_ref_no = generate_unique_customerRef()
        ledgermodel.bank_partner_id = decResp.get("bank_partner_id")
        ledgermodel.van = " "
        startYear = int(decResp.get("credit_date")[0:4])
        startMonth = int(decResp.get("credit_date")[5:7])
        startDay = int(decResp.get("credit_date")[8:10])
        startHours = int(decResp.get("credit_date")[11:13])
        startMinute = int(decResp.get("credit_date")[14:16])
        dt = datetime.now()
        start = dt.replace(year=startYear, day=startDay, month=startMonth, hour=startHours, minute=startMinute,
                           second=0, microsecond=0)
        ledgermodel.credit_transaction_date = start
        ledgermodel.bene_account_name = const.bene_account_name
        ledgermodel.bene_account_number = const.bene_account_number
        ledgermodel.bene_ifsc = const.bene_ifsc
        ledgermodel.createdBy = "adminID :: " + str(admin)
        ledgermodel.created_at = datetime.now()
        ledgermodel.status = True
        ledgermodel.charge = charge.get("total_charge")
        ledgermodel.tax = charge.get("total_tax")
        ledgermodel.trans_status = "Success"  # success
        ledgermodel.payout_trans_id = linkedId
        ledgermodel.is_tax_inclusive = decResp.get("is_tax_inclusive")
        ledgermodel.trans_init_time = datetime.now()
        ledgermodel.trans_completed_time = datetime.now()
        ledgermodel.total_amount = amount - float(charge.get("total_charge") + charge.get("total_tax"))
        ledgermodel.save()
        # {"total_charge":charge,
        # "base_bank_charge":base_bank_charge,
        # "base_sabpaisa_convenience_fee":base_sabpaisa_convenience_fee,
        # "bankTax":bankTax,
        # "sabpaisa_convenience_fee_tax":sabpaisa_convenience_fee_tax,
        # "total_tax":total_tax}  
        if (charge.get("base_bank_charge") > 0):
            chargeBreakService = Charge_Breaking_model_services(charge_amount=charge.get("base_bank_charge"),
                                                                transaction_id=ledgermodel.id,
                                                                charge_type="bank charge",
                                                                payout_transaction_id=ledgermodel.payout_trans_id,
                                                                tax_amount=charge.get("bankTax"), charge_id=0)
            chargeBreakService.save()
        if (charge.get("base_sabpaisa_convenience_fee") > 0):
            chargeBreakService = Charge_Breaking_model_services(
                charge_amount=charge.get("base_sabpaisa_convenience_fee"), transaction_id=ledgermodel.id,
                charge_type="sp convinience charge", payout_transaction_id=ledgermodel.payout_trans_id,
                tax_amount=charge.get("sabpaisa_convenience_fee_tax"), charge_id=0)
            chargeBreakService.save()
        if (charge.get("base_bank_charge") > 0 or charge.get("base_sabpaisa_convenience_fee") > 0):
            chargeBreakService = Charge_Breaking_model_services(charge_amount=charge.get("total_tax"),
                                                                transaction_id=ledgermodel.id, charge_type="total tax",
                                                                payout_transaction_id=ledgermodel.payout_trans_id,
                                                                tax_amount=0, charge_id=0)
            chargeBreakService.save()

        log_service.table_id = ledgermodel.id
        log_service.save()
        return str(ledgermodel.id)

    @staticmethod
    def addCharge(decResp, client_ip_address, admin, amount, linkedId):
        charge = float()
        tax = TaxModel.objects.filter(status=True).values()[0].get("tax")
        is_tax_inclusive = decResp.get("is_tax_inclusive")
        total_tax = float()
        bank_charge = float(decResp.get("bank_charge"))
        is_charged_by_bank = float(decResp.get("is_charged_by_bank"))
        sabpaisa_convenience_fee = float(decResp.get("sabpaisa_convenience_fee"))
        sabpaisa_convenience_fee_tax = float()
        base_sabpaisa_convenience_fee = float()
        base_sabpaisa_convenience_fee = 0.0
        bankTax = float()
        base_bank_charge = float()
        charge = 0.0
        total_tax = 0.0
        base_bank_charge = 0.0
        if (bank_charge < 0.01 and sabpaisa_convenience_fee < 0.01):
            return {"total_charge": charge,
                    "base_bank_charge": base_bank_charge,
                    "base_sabpaisa_convenience_fee": base_sabpaisa_convenience_fee,
                    "bankTax": bankTax,
                    "sabpaisa_convenience_fee_tax": sabpaisa_convenience_fee_tax,
                    "total_tax": total_tax}
        if (bank_charge != 0 or bank_charge != 0.0 or bank_charge != 0.00):
            if (is_charged_by_bank == True):
                base_bank_charge = formulas.calulate_base(bank_charge, tax)
                bankTax = bank_charge - base_bank_charge

            else:
                if (is_tax_inclusive == True):
                    base_bank_charge = formulas.calulate_base(bank_charge, tax)
                    bankTax = bank_charge - base_bank_charge
                    total_tax = bankTax

                else:
                    base_bank_charge = bank_charge
                    bankTax = formulas.calulate_tax_exclusive(bank_charge, float(tax))

        if (sabpaisa_convenience_fee != 0 or sabpaisa_convenience_fee != 0.0 or sabpaisa_convenience_fee != 0.00):
            if (is_tax_inclusive == False):
                base_sabpaisa_convenience_fee = float(sabpaisa_convenience_fee)
                # charge = base_bank_charge+base_sabpaisa_convenience_fee
                sabpaisa_convenience_fee_tax = formulas.calulate_tax_exclusive(base_sabpaisa_convenience_fee,
                                                                               float(tax))
                # total_tax = bankTax+sabpaisa_convenience_fee_tax

            else:
                sabpaisa_convenience_fee = float(sabpaisa_convenience_fee)
                base_sabpaisa_convenience_fee = formulas.calulate_base(float(sabpaisa_convenience_fee), float(tax))

                sabpaisa_convenience_fee_tax = sabpaisa_convenience_fee - base_sabpaisa_convenience_fee

        # if(decResp.get("is_tax_inclusive")==False):
        #     if(bank_charge!="" and sabpaisa_convenience_fee!=""):
        #         bank_charge =  float(bank_charge)
        #         sabpaisa_convenience_fee =  float(sabpaisa_convenience_fee)
        #         charge = bank_charge+sabpaisa_convenience_fee
        #         bankTax = formulas.calulate_tax_exclusive(bank_charge,float(tax))
        #         sabpaisa_convenience_fee_tax = formulas.calulate_tax_exclusive(sabpaisa_convenience_fee,float(tax)) 
        #         total_tax = bankTax+sabpaisa_convenience_fee_tax
        #         Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=sabpaisa_convenience_fee,client_ip_address=client_ip_address,tax=sabpaisa_convenience_fee_tax,trans_type="charge",linkedId=linkedId) 
        #         Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=bank_charge,client_ip_address=client_ip_address,tax=bankTax,is_chargedBy_bank=decResp.get("is_charged_by_bank"),trans_type="charge",linkedId=linkedId)
        #     elif(bank_charge!="" or sabpaisa_convenience_fee!=""):
        #         if(bank_charge==""and sabpaisa_convenience_fee!=""):
        #             sabpaisa_convenience_fee =  float(sabpaisa_convenience_fee)
        #             bank_charge = 0
        #             bankTax = 0
        #             sabpaisa_convenience_fee_tax = formulas.calulate_tax_exclusive(sabpaisa_convenience_fee,float(tax)) 
        #             Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=sabpaisa_convenience_fee,client_ip_address=client_ip_address,tax=sabpaisa_convenience_fee_tax,trans_type="charge",linkedId=linkedId) 
        #         if(sabpaisa_convenience_fee=="" and bank_charge!=""):
        #             bank_charge =  float(bank_charge)
        #             sabpaisa_convenience_fee=0
        #             sabpaisa_convenience_fee_tax=0
        #             bankTax = formulas.calulate_tax_exclusive(bank_charge,float(tax))
        #             Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=bank_charge,client_ip_address=client_ip_address,tax=bankTax,is_chargedBy_bank=decResp.get("is_charged_by_bank"),trans_type="charge",linkedId=linkedId)
        #         charge = bank_charge+sabpaisa_convenience_fee
        #         total_tax = sabpaisa_convenience_fee_tax+bankTax
        #     print("total tax "+str(total_tax)+" charge "+str(charge))
        # else:
        #         if(bank_charge!="" and sabpaisa_convenience_fee!=""):
        #             bank_charge =  float(bank_charge)
        #             sabpaisa_convenience_fee =  float(sabpaisa_convenience_fee)
        #             base_sabpaisa_convenience_fee= formulas.calulate_base(float(sabpaisa_convenience_fee),float(tax))
        #             base_bank_charge = formulas.calulate_base(float(bank_charge),float(tax))
        #             charge = base_bank_charge+base_sabpaisa_convenience_fee
        #             bankTax = bank_charge-base_bank_charge
        #             sabpaisa_convenience_fee_tax = sabpaisa_convenience_fee-base_sabpaisa_convenience_fee
        #             total_tax = bankTax+sabpaisa_convenience_fee_tax
        #             Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=base_sabpaisa_convenience_fee,client_ip_address=client_ip_address,tax=sabpaisa_convenience_fee_tax,trans_type="charge",linkedId=linkedId) 
        #             Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=base_bank_charge,client_ip_address=client_ip_address,tax=bankTax,is_chargedBy_bank=decResp.get("is_charged_by_bank"),trans_type="charge",linkedId=linkedId)
        #         elif(bank_charge!="" or sabpaisa_convenience_fee!=""):

        #             if(bank_charge==""and sabpaisa_convenience_fee!=""):
        #                 sabpaisa_convenience_fee =  float(sabpaisa_convenience_fee)
        #                 base_sabpaisa_convenience_fee= formulas.calulate_base(float(sabpaisa_convenience_fee),float(tax))
        #                 bank_charge = 0
        #                 bankTax = 0
        #                 sabpaisa_convenience_fee_tax = sabpaisa_convenience_fee-base_sabpaisa_convenience_fee
        #                 Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=base_sabpaisa_convenience_fee,client_ip_address=client_ip_address,tax=sabpaisa_convenience_fee_tax,trans_type="charge",linkedId=linkedId) 

        #             if(sabpaisa_convenience_fee=="" and bank_charge!=""):
        #                 bank_charge =  float(bank_charge)
        #                 base_bank_charge = formulas.calulate_base(float(bank_charge),float(tax))
        #     sabpaisa_convenience_fee=0
        #     sabpaisa_convenience_fee_tax=0
        #     bankTax = bank_charge-base_bank_charge
        #     Ledger_Model_Service().saveCharge(decResp=decResp,admin=admin,amount=base_bank_charge,client_ip_address=client_ip_address,tax=bankTax,is_chargedBy_bank=decResp.get("is_charged_by_bank"),trans_type="charge",linkedId=linkedId)

        # charge = bank_charge+sabpaisa_convenience_fee
        # total_tax = sabpaisa_convenience_fee_tax+bankTax
        charge = base_bank_charge + base_sabpaisa_convenience_fee
        total_tax = bankTax + sabpaisa_convenience_fee_tax
        return {"total_charge": charge,
                "base_bank_charge": base_bank_charge,
                "base_sabpaisa_convenience_fee": base_sabpaisa_convenience_fee,
                "bankTax": bankTax,
                "sabpaisa_convenience_fee_tax": sabpaisa_convenience_fee_tax,
                "total_tax": total_tax}

    def fetchInfo():
        cursors = connection.cursor()
        #
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="cr" and  trans_status in ("Success") and trans_date =  CURDATE();')
        credit_amount = cursors.fetchone()[0]
        if credit_amount == None:
            credit_amount = 0
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="dr" and  trans_status in ("Success","Pending","Requested","Proccesing") and trans_date =  CURDATE();;')
        debited_amount = cursors.fetchone()[0]
        if debited_amount == None:
            debited_amount = 0
        #
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="cr" and  trans_status in ("Success");')
        credit_amount_1 = cursors.fetchone()[0]
        if credit_amount_1 == None:
            credit_amount_1 = 0
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="dr" and  trans_status in ("Success","Pending","Requested","Proccesing");')
        debited_amount_1 = cursors.fetchone()[0]
        if debited_amount_1 == None:
            debited_amount_1 = 0
        # getBalance(merchant_id,client_ip_address,created_by):
        total_balance = credit_amount_1 - debited_amount_1
        cursors.execute(
            "select count(merchant_id) as c from apis_transactionhistorymodel where trans_date =  CURDATE();")
        total_transactions = cursors.fetchone()[0]
        if total_transactions == None:
            total_transactions = 0
        total_merchant = len(MerchantModel.objects.all())
        # cursors.execute("select count(merchant_id) from apis_transactionhistorymodel where trans_date =  CURDATE() ")

        # total_merchants = cursors.fetchone()[0]
        # if total_merchants==None:
        #     total_merchants=0
        cursors.execute("call todayTransactingMerchant();")
        transacting_merchant = cursors.fetchone()[0]
        if transacting_merchant == None:
            transacting_merchant = 0
        resp = {
            "credit_amount": credit_amount,
            "debited_amount": debited_amount,
            "total_merchants": total_merchant,
            "total_balance": total_balance,
            "total_transactions": total_transactions,
            "transacting_merchant": transacting_merchant
        }
        return resp

    @staticmethod
    def saveCharge(decResp, amount, admin, client_ip_address, linkedId, is_chargedBy_bank=None, tax=None,
                   trans_type=None):
        log_service = Log_model_services.Log_Model_Service(log_type="create", table_name="apis_ledgermodel",
                                                           remarks="saving records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip,
                                                           created_by=decResp.get("created_by"))
        ledgermodel = LedgerModel()
        ledgermodel.amount = amount
        modeOfTrans = decResp.get("mode")
        m = ModeModel.objects.filter(mode=modeOfTrans)
        ledgermodel.payment_mode_id = m[0].id
        ledgermodel.bank_ref_no = decResp.get("bank_ref_no")
        ledgermodel.trans_amount_type = "dr"
        ledgermodel.trans_type = trans_type
        ledgermodel.type_status = "Generated"
        ledgermodel.trans_date = date.today()
        ledgermodel.request_header = "request header"
        bankResp = "NULL"
        ledgermodel.purpose = "DEBITED FOR " + trans_type
        ledgermodel.remarks = decResp.get("remarks")
        ledgermodel.merchant_id = decResp.get("merchant_id")
        ledgermodel.client_code = "null"
        # CR06e65070-dbd6-11eb-9816-507b9d006cb8
        ledgermodel.customer_ref_no = generate_unique_customerRef()
        ledgermodel.bank_partner_id = decResp.get("bank_partner_id")
        ledgermodel.van = " "
        startYear = int(decResp.get("credit_date")[0:4])
        startMonth = int(decResp.get("credit_date")[5:7])
        startDay = int(decResp.get("credit_date")[8:10])
        startHours = int(decResp.get("credit_date")[11:13])
        startMinute = int(decResp.get("credit_date")[14:16])
        dt = datetime.now()
        start = dt.replace(year=startYear, day=startDay, month=startMonth, hour=startHours, minute=startMinute,
                           second=0, microsecond=0)
        ledgermodel.credit_transaction_date = start
        ledgermodel.bene_account_name = const.bene_account_name
        ledgermodel.bene_account_number = const.bene_account_number
        ledgermodel.linked_Txn_id = linkedId
        ledgermodel.bene_ifsc = const.bene_ifsc
        ledgermodel.createdBy = "adminID :: " + str(admin)
        ledgermodel.created_at = datetime.now()
        ledgermodel.status = True
        ledgermodel.trans_status = "Success"  # success
        ledgermodel.tax = tax
        ledgermodel.payout_trans_id = generate_token()
        ledgermodel.is_charged_by_bank = is_chargedBy_bank
        ledgermodel.is_tax_inclusive = decResp.get("is_tax_inclusive")
        ledgermodel.save()
        log_service.table_id = ledgermodel.id
        log_service.save()
        return str(ledgermodel.id)
        # debit crredit

    def merchantCreditDebit(merchant_id, client_ip_address, created_by):
        cursors = connection.cursor()
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="cr" and  trans_status in ("Success") and merchant_id=' + str(
                merchant_id) + ';')
        credit_amount_1 = cursors.fetchone()[0]
        if credit_amount_1 == None:
            credit_amount_1 = 0
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="dr" and  trans_status in ("Success","Pending","Requested","Proccesing")and merchant_id=' + str(
                merchant_id) + ';')
        debited_amount_1 = cursors.fetchone()[0]
        if debited_amount_1 == None:
            debited_amount_1 = 0
        total_balance = credit_amount_1 - debited_amount_1
        resp = {
            "credit_amount": credit_amount_1,
            "debited_amount": debited_amount_1,
            "total_balance": total_balance,
        }
        return resp

    def AllCreditDebit(merchant_id, client_ip_address, created_by):
        cursors = connection.cursor()
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="cr" and  trans_status in ("Success");')
        credit_amount_1 = cursors.fetchone()[0]
        if credit_amount_1 == None:
            credit_amount_1 = 0
        cursors.execute(
            'select sum(total_amount) from apis_transactionhistorymodel where trans_amount_type="dr" and  trans_status in ("Success","Pending","Requested","Proccesing");')
        debited_amount_1 = cursors.fetchone()[0]
        if debited_amount_1 == None:
            debited_amount_1 = 0
        total_balance = credit_amount_1 - debited_amount_1
        resp = {
            "credit_amount": credit_amount_1,
            "debited_amount": debited_amount_1,
            "total_balance": total_balance,
        }
        return resp
