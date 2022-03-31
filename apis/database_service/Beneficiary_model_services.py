from apis import const
from apis.database_models.ChangeModel import ChargeModel
from apis.database_service import Log_model_services
from ..database_models.BeneficiaryModel import BeneficiaryModel


class Beneficiary_Model_Services:
    def __init__(self, full_name=None, account_number=None, upiId=None, ifsc_code=None, merchant_id=None,
                 bank_name=None, category=None):
        self.full_name = full_name
        self.account_number = account_number
        self.upiId = upiId
        self.ifsc_code = ifsc_code
        self.merchant_id = merchant_id
        self.bank_name = bank_name
        self.category = category

    def save(self):
        beneficiarymodel = BeneficiaryModel()
        beneficiarymodel.full_name = self.full_name
        beneficiarymodel.account_number = self.account_number
        beneficiarymodel.upi_id = self.upiId
        beneficiarymodel.ifsc_code = self.ifsc_code
        beneficiarymodel.merchant_id = self.merchant_id
        beneficiarymodel.created_by = "merchant id :: " + str(self.merchant_id)
        beneficiarymodel.bank_name = self.bank_name
        beneficiarymodel.category = self.category
        beneficiarymodel.save()
        return beneficiarymodel

    @staticmethod
    def soft_delete_by_id(id):
        ben = BeneficiaryModel.objects.get(id=id)
        ben.status = False
        ben.save()

    @staticmethod
    def fetch_by_upiId(merchant_id, upi_id):
        beneficiarymodel = BeneficiaryModel.objects.get(merchant_id=merchant_id, upi_id=upi_id, status=True)
        # if len(beneficiarymodel)==0:
        #     return None

        return beneficiarymodel

    @staticmethod
    def fetch_by_id(id):
        beneficiarymodel = BeneficiaryModel.objects.get(id=id, status=True)
        return beneficiarymodel

    @staticmethod
    def fetch_by_account_number_ifsc(merchant_id, account_number, ifsc):
        beneficiarymodel = BeneficiaryModel.objects.filter(status=True, merchant_id=merchant_id,
                                                           account_number=account_number, ifsc_code=ifsc)
        if len(beneficiarymodel) == 0:
            return None
        return beneficiarymodel

    def update(self, updated_by, updated_at, id, created_at):
        beneficiarymodel = BeneficiaryModel.objects.get(id=id)
        beneficiarymodel.full_name = self.full_name
        beneficiarymodel.upi_id = self.upiId
        beneficiarymodel.account_number = self.account_number
        beneficiarymodel.ifsc_code = self.ifsc_code
        beneficiarymodel.merchant_id = self.merchant_id
        beneficiarymodel.updated_at = updated_at
        beneficiarymodel.created_at = created_at
        beneficiarymodel.updated_by = updated_by
        beneficiarymodel.save()

    @staticmethod
    def fetchBeneficiaryByMerchantId(merchant_id):
        beneficarymodel = BeneficiaryModel.objects.filter(merchant_id=merchant_id)
        if len(beneficarymodel) == 0:
            return None
        return beneficarymodel

    @staticmethod
    def fetchBeneficiaryByParams(client_ip_address, created_by, page, length, merchant_id=None):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_chargemodel",
                                                           remarks="fetching records from apis_chargemodel by primary key in the record",
                                                           client_ip_address=client_ip_address,
                                                           server_ip_address=const.server_ip, created_by=created_by)
        offSet = (int(page) - 1) * int(length)
        chargeModel = BeneficiaryModel.objects.raw(
            "select * from apis_beneficiarymodel where merchant_id = " + merchant_id + " order by id desc  limit " + str(
                length) + " offset " + str(offSet))
        resp = list()
        for data in list(chargeModel.iterator()):
            d = {
                "id": data.id,
                "full_name": data.full_name,
                "account_number": data.account_number,
                "ifsc_code": data.ifsc_code,
                "merchant_id": data.merchant_id,
                "created_at": data.created_at,
                "upiId": data.upi_id,
                "deleted_at": data.deleted_at,
                "updated_at": data.updated_at,
                "created_by": data.created_by,
                "deleted_by": data.deleted_by,
                "updated_by": data.updated_by,
            }
            resp.append(d)
        log_service.save()
        return resp
