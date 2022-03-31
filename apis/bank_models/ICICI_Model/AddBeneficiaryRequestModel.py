from apis.database_models.BeneficiaryModel import BeneficiaryModel
from apis.database_models.IciciBeneficiaryModel import ICICI_Beneficiary
import uuid


class BeneficiaryRequestModel:
    CrpId = None
    CrpUsr = None
    BnfName = None
    BnfNickName = None
    BnfAccNo = None
    IFSC = None
    AGGR_ID = None
    URN = None
    PayeeType = None

    def __init__(self, CrpId="", CrpUsr="", BnfName="", BnfNickName="", BnfAccNo="", IFSC="", AGGR_ID="", URN="",
                 PayeeType=""):
        self.CrpId = CrpId
        self.CrpUsr = CrpUsr
        self.BnfName = BnfName
        self.BnfNickName = BnfNickName
        self.BnfAccNo = BnfAccNo
        self.IFSC = IFSC
        self.AGGR_ID = AGGR_ID
        self.URN = URN
        self.PayeeType = PayeeType

    # function to convert the class object to json
    def to_json(self):
        return {
            "CrpId": self.CrpId,
            "CrpUsr": self.CrpUsr,
            "BnfName": self.BnfName,
            "BnfNickName": self.BnfNickName,
            "BnfAccNo": self.BnfAccNo,
            "IFSC": self.IFSC,
            "AGGR_ID": self.AGGR_ID,
            "URN": self.URN,
            "PayeeType": self.PayeeType
        }

    # function to convert the json to class object
    @staticmethod
    def from_json(json_object):
        return BeneficiaryRequestModel(
            CrpId=json_object.get("CrpId", ""),
            CrpUsr=json_object.get("CrpUsr", ""),
            BnfName=json_object.get("BnfName", ""),
            BnfNickName=json_object.get("BnfNickName", ""),
            BnfAccNo=json_object.get("BnfAccNo", ""),
            IFSC=json_object.get("IFSC", ""),
            AGGR_ID=json_object.get("AGGR_ID", ""),
            URN=json_object.get("URN", ""),
            PayeeType=json_object.get("payeeType", "")
        )

    # function to create BeneficiaryRequestModel from BeneficiaryModel and ICICI_Beneficiary
    @staticmethod
    def from_beneficiary_model(beneficiary_model: BeneficiaryModel, icici_beneficiary: ICICI_Beneficiary):
        return BeneficiaryRequestModel(
            CrpId=icici_beneficiary.corpId,
            CrpUsr=icici_beneficiary.corpUsr,
            BnfName=beneficiary_model.full_name,
            BnfNickName=beneficiary_model.full_name.replace(" ", ""),
            # BnfNickName="RakeshSourabhRT2Test11",
            BnfAccNo=beneficiary_model.account_number,
            IFSC=beneficiary_model.ifsc_code,
            AGGR_ID=icici_beneficiary.aggrId,
            URN=icici_beneficiary.URN,
            PayeeType=icici_beneficiary.payeeType
        )
