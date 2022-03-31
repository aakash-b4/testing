from rest_framework import status

from datetime import datetime
from sabpaisa import auth
from rest_framework.permissions import AND
from ...models import LedgerModel
from django.db import connection


class ICICI_service:
    def __init__(self, id=None, client_id=None, client_code=None, type_status=None, amount=None, van=None, trans_type=None, trans_status=None, bank_ref_no=None, customer_ref_no=None, bank_id=None, trans_time=None, bene_account_name=None, bene_account_number=None, bene_ifsc=None, request_header=None, createdBy=None, updatedBy=None, deletedBy=None, created_at=None, deleted_at=None, updated_at=None, status=True, mode=None, charge=None):
        self.id = id
        self.client_id = client_id
        self.client_code = client_code
        self.amount = amount
        self.trans_type = trans_type
        self.trans_status = trans_status
        self.bank_ref_no = bank_ref_no
        self.customer_ref_no = customer_ref_no
        self.bank_id = bank_id
        self.trans_time = trans_time
        self.type_status = type_status
        self.bene_account_name = bene_account_name
        self.bene_account_number = bene_account_number
        self.bene_ifsc = bene_ifsc
        self.request_header = request_header
        self.van = van
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        self.deletedBy = deletedBy
        self.created_at = created_at
        self.deleted_at = deleted_at
        self.updated_at = updated_at
        self.status = status
        self.mode = mode
        self.charge = charge

    def save(self):
        ledgermodel = LedgerModel()
        ledgermodel.client = self.client_id
        ledgermodel.client_code = self.client_code
        ledgermodel.amount = self.amount
        ledgermodel.trans_type = self.trans_type
        ledgermodel.type_status = self.type_status
        ledgermodel.trans_status = self.trans_status
        ledgermodel.bank_ref_no = self.bank_ref_no
        ledgermodel.customer_ref_no = self.customer_ref_no
        ledgermodel.bank = self.bank_id
        ledgermodel.trans_time = self.trans_time
        ledgermodel.van = self.van
        ledgermodel.bene_account_name = self.bene_account_name
        ledgermodel.bene_account_number = self.bene_account_number
        ledgermodel.bene_ifsc = self.bene_ifsc
        ledgermodel.request_header = self.request_header
        ledgermodel.createdBy = self.createdBy
        ledgermodel.updatedBy = self.updatedBy
        ledgermodel.deletedBy = self.deletedBy
        ledgermodel.created_at = self.created_at
        ledgermodel.deleted_at = self.deleted_at
        ledgermodel.updated_at = self.updated_at
        ledgermodel.status = self.status
        ledgermodel.mode = self.mode
        ledgermodel.charge = self.charge
        ledgermodel.save()
        # resp =
        return ledgermodel.id

    def fetch_by_clientid(self, client_id):
        ledgerModels = LedgerModel.objects.filter(client=client_id)
        return ledgerModels

    def fetch_by_clientcode(self, client_code):
        ledgerModels = LedgerModel.objects.filter(client_code=client_code)
        return ledgerModels

    def fetch_by_id(self, id):
        ledgerModels = LedgerModel.objects.get(id=id)
        return ledgerModels

    def fetch_by_van(self, van):
        ledgerModels = LedgerModel.objects.filter(van=van)
        return ledgerModels
    # def update_status(self,id,status):
    #     ledgerModel=LedgerModel.objects.get(id=id)
    #     ledgerModel.trans_status=status
    #     return ledgerModel

    # def fetchAll(self):
    #     ledgerModel = LedgerModel.objects.filter(status=True)
    #     return ledgerModel
    def deleteLedger(self, id):
        LedgerModel.objects.filter(id=id).delete()
        return True

    def getBalance(self, clientCode):
        cursors = connection.cursor()
        cursors.execute("getBalance("+clientCode+",@balance)")
        cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        return value

    def fetchAll():
        ledgerModel = LedgerModel.objects.filter(status=True)
        return ledgerModel

    def deleteById(id, deletedBy):
        ledger = LedgerModel.objects.filter(id=id)
        print("service ledger = ", ledger)
        if(len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            print("service     ", ledgerModel)
            ledgerModel.status = False
            ledgerModel.deletedBy = deletedBy
            ledgerModel.deleted_at = datetime.now()
            ledgerModel.save()
            return True
        return False

    def findById(id):
        ledger = LedgerModel.objects.filter(id=id)
        if(len(ledger) > 0):
            return True
        else:
            return False

    def findByClientCodeService(clientCode):
        ledgerModel = LedgerModel.objects.filter(client_code=clientCode)
        return ledgerModel

    def findByClientIdService(clientId):
        ledgerModel = LedgerModel.objects.filter(client=clientId)
        return ledgerModel

    def findByTransTimeService(startTranstime, endTransTime):
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
        start = dt.replace(year=startYear, day=startDay, month=startMonth,
                           hour=startHours, minute=startMinute, second=0, microsecond=0)
        end = dt.replace(year=endYear, day=endDay, month=endMonth,
                         hour=endHours, minute=endMinute, second=0, microsecond=0)
        ledger = LedgerModel.objects.filter(trans_time__range=[start, end])
        print("start = ", start)
        print("end = ", end)
        print("date ======= ", ledger)
        return ledger

    def update(self):
        ledgermodel = LedgerModel()
        ledgermodel.id = self.id
        ledgermodel.client = self.client_id
        ledgermodel.client_code = self.client_code
        ledgermodel.amount = self.amount
        ledgermodel.trans_type = self.trans_type
        ledgermodel.type_status = self.type_status
        ledgermodel.trans_status = self.trans_status
        ledgermodel.bank_ref_no = self.bank_ref_no
        ledgermodel.customer_ref_no = self.customer_ref_no
        ledgermodel.bank = self.bank_id
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
        ledgermodel.status = self.status
        ledgermodel.mode = self.mode
        ledgermodel.charge = self.charge
        ledgermodel.save()
        return ledgermodel.id


def enc(encStr, authKey, authIV):
    authobj = auth.AESCipher(authKey, authIV)
    encStr = authobj.encrypt(encStr)
    encStr = str(encStr)
    return encStr
