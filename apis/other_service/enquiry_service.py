from django.db.models import query
from django.http import response
from apis.database_service.Ledger_model_services import Ledger_Model_Service
from apis import const
from sabpaisa import auth
from datetime import datetime
from apis.database_service import Log_model_services
from ..database_service import Client_model_service
from ..models import TransactionHistoryModel as LedgerModel
from django.db import connection
import math


class enquiry_service:
    def fetch_by_van(self, van):
        ledgerModels = LedgerModel.objects.filter(van=van)
        return ledgerModels

    def deleteLedger(self, id):
        LedgerModel.objects.filter(id=id).delete()
        return True

    def getBalance(self, clientCode):
        cursors = connection.cursor()
        cursors.execute("getBalance(" + clientCode + ",@balance)")
        cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        return value

    def fetchAll(clientCode, createdBy, ip):
        clientModel = Client_model_service.Client_Model_Service.fetch_by_clientcode(client_ip_address=ip,
                                                                                    client_code=clientCode,
                                                                                    created_by=createdBy)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        ledgerModel = LedgerModel.objects.filter(status=True)
        if (len(ledgerModel) == 0):
            return "0"
        resp = str(list(ledgerModel.values()))
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return encResp

    def deleteById(id, deletedBy):
        ledger = LedgerModel.objects.filter(id=id)
        print("service ledger = ", ledger)
        if (len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            print("service     ", ledgerModel)
            ledgerModel.status = False
            ledgerModel.deletedBy = deletedBy
            ledgerModel.deleted_at = datetime.now()
            ledgerModel.save()
            return True
        return False

    def findByTransTimeService(startTranstime, endTransTime, merchant, created_by, client_ip_address):
        startYear = int(startTranstime[0:4])
        startMonth = int(startTranstime[5:7])
        startDay = int(startTranstime[8:10])
        startHours = int(startTranstime[11:13])
        startMinute = int(startTranstime[14:16])

        endYear = int(endTransTime[0:4])
        endMonth = int(endTransTime[5:7])
        endDay = int(endTransTime[8:10])
        endHours = int(endTransTime[11:13])
        endMinute = int(endTransTime[14:16])

        dt = datetime.now()
        start = dt.replace(year=startYear, day=startDay, month=startMonth, hour=startHours, minute=startMinute,
                           second=0, microsecond=0)
        end = dt.replace(year=endYear, day=endDay, month=endMonth, hour=endHours, minute=endMinute, second=0,
                         microsecond=0)
        Ledger = LedgerModel.objects.filter(trans_time__range=[start, end])
        if (len(Ledger) == 0):
            return "0"
        resp = str(list(Ledger.values()))
        return resp

    @staticmethod
    def get_enc(merchant_id, customer_ref, client_ip_address, created_by):
        rec = Ledger_Model_Service.fetch_customer_ref_no(merchant=merchant_id, customer_ref_no=customer_ref,
                                                         client_ip_address=client_ip_address, created_by=created_by)
        print(rec)
        if len(rec) == 0:
            return None
        return rec

    @staticmethod
    def fetchLedgerByParams(merchant, created_by, client_ip_address, page, length, client_code=None,
                            customer_ref_no=None, startTime=None, endTime=None, trans_type=None):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel",
                                                           remarks="fetching records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)
        log_service.save()
        resp = LedgerModel.objects.filter(merchant=merchant).values()
        if (length == "all"):
            return resp
        if (int(length) > len(resp)):
            return resp
        length = int(length)
        splitlen = math.ceil(len(resp) / length)
        split_list = []
        for i in range(splitlen):
            split_list.append(resp[length * i:length * (i + 1)])
        json = {
            "data": str(split_list[int(page) - 1]),
            "splitlen": str(splitlen)
        }
        respJson = str(json)
        return split_list[int(page) - 1]
