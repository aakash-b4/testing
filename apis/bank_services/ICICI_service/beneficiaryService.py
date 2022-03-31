import json
import re
import traceback

from apis.bank_conf.config import Configuration
from apis.bank_models.ICICI_Model.AddBeneficiaryRequestModel import BeneficiaryRequestModel
from apis.bank_services.ICICI_service import utils
from apis.database_models.BeneficiaryModel import BeneficiaryModel
from apis.database_models.CIBRegistrationModel import CIBRegistration
from apis.database_models.ClientModel import MerchantModel
from apis.database_models.IciciBeneficiaryModel import ICICI_Beneficiary
from apis.bank_services.ICICI_service import utils


def register_beneficiary(beneficiary_model: BeneficiaryModel, icici_beneficiary: ICICI_Beneficiary):
    print("============== registering icici beneficiary through account and ifsc code ================")
    icici_bene = None
    try:
        icici_bene = ICICI_Beneficiary.objects.get(
            corpId=icici_beneficiary.corpId, corpUsr=icici_beneficiary.corpUsr, aggrId=icici_beneficiary.aggrId,
            merchantId=icici_beneficiary.merchantId, payout_beneficiary_id=icici_beneficiary.payout_beneficiary_id)
    except ICICI_Beneficiary.DoesNotExist:
        print("beneficiary does not exist")
    if icici_bene:
        icici_beneficiary = icici_bene
        if icici_beneficiary.ifsc_registered:
            return {"status": True, "data": icici_beneficiary.to_json()}
    else:
        icici_beneficiary.save()
    beneficiary_request_model = BeneficiaryRequestModel.from_beneficiary_model(
        beneficiary_model, icici_beneficiary)
    # Convert the BeneficiaryRequestModel to json
    beneficiary_request_json = beneficiary_request_model.to_json()

    url = Configuration.get_Property("ICICI_AddBeneficiaryURL")

    request_data = utils.create_icici_request(beneficiary_request_json)
    request = utils.send_request(url=url, data=request_data, type="POST")
    try:
        bank_response = request.json()

        if 'encryptedKey' in bank_response:
            bank_response = json.loads(utils.decrypt_data(bank_response))

        bank_response = {key.lower(): value for key,
                                                value in bank_response.items()}
        try:
            if bank_response["response"].lower() == "success" and "bnf_id" in bank_response:
                # Convert the response to BeneficiaryResponseModel
                icici_beneficiary.response = bank_response.get(
                    "response", None)
                icici_beneficiary.message = bank_response.get(
                    "message", None)
                icici_beneficiary.bnfId = bank_response.get("BNF_ID".lower(), None)
                icici_beneficiary.ifsc_registered = True
                icici_beneficiary.save()
                return {"status": True, "data": icici_beneficiary.to_json()}
            else:
                icici_beneficiary.success = bank_response.get('success', None)
                icici_beneficiary.response = bank_response.get('response', None)
                icici_beneficiary.message = bank_response.get('message', None)
                icici_beneficiary.errorMessage = bank_response.get(
                    'errormessage', None)
                icici_beneficiary.save()
                return {"status": False, "data": icici_beneficiary.to_json()}
        except Exception as e:
            print(traceback.format_exc())
            icici_beneficiary.success = bank_response.get('success', None)
            icici_beneficiary.response = bank_response.get('response', None)
            icici_beneficiary.message = bank_response.get('message', None)
            icici_beneficiary.errorMessage = bank_response.get(
                'errormessage', None)
            icici_beneficiary.save()
            return {"status": False, "data": icici_beneficiary.to_json()}
    except:
        print("Exception in adding benefifciary in icici bank")
        traceback.print_exc()
        bank_response = request.text
        icici_beneficiary.response = request.text
        icici_beneficiary.save()
        # Return the BeneficiaryResponseModel
        return {"status": False, "data": icici_beneficiary.to_json()}


def register_beneficiary_vpa(bene_data: dict):
    print("============== registering icici beneficiary through vpa ================")
    url = Configuration.get_Property("ICICI_VpaBeneficiaryURL")

    request_data = utils.create_icici_request(bene_data)
    request = utils.send_request(url=url, data=request_data, type="POST")
    bank_response = {}
    try:
        bank_response = request.json()
        if 'encryptedKey' in bank_response:
            bank_response = json.loads(utils.decrypt_data(bank_response))
        bank_response = {key.lower(): value for key,
                                                value in bank_response.items()}

        try:
            if bank_response["response"].lower() == "success" and "bnf_id" in bank_response:
                bank_response["response"] = bank_response.get(
                    "response", None)
                bank_response["message"] = bank_response.get(
                    "message", None)
                bank_response["bnfId"] = bank_response.get("BNF_ID".lower(), None)
                bank_response["vpa_registered"] = True
                return {"status": True, "data": bank_response}
        except Exception as e:
            print(traceback.format_exc())
            bank_response["success"] = bank_response.get('success', None)
            bank_response["response"] = bank_response.get('response', None)
            bank_response["message"] = bank_response.get('message', None)
            bank_response["errorMessage"] = bank_response.get(
                'errormessage', None)
            bank_response["vpa_registered"] = False
            return {"status": False, "data": bank_response}
    except:
        print("Exception in adding benefifciary through vpa in icici bank")
        traceback.print_exc()
        bank_response["response"] = request.text
        bank_response["vpa_registered"] = False
        # Return the BeneficiaryResponseModel
        return {"status": False, "data": bank_response}


def getBeneficiaryByMerchantId(id: int):
    return ICICI_Beneficiary.objects.get(merchantId=id)


def create_icici_bene_request_data(bene_data: dict) -> dict:
    request_data = {}

    merchant = bene_data.get("merchant")
    if merchant.default_account == "MERCHANT":
        cib_registration = CIBRegistration.objects.get(merchantId=bene_data['merchant_id'])
    elif merchant.default_account == "SABPAISA":
        cib_registration = CIBRegistration.objects.get(merchantId=getSabpaisaMerchantId())
    if not cib_registration:
        return {"status": False, "message": "Merchant is not registered with CIB"}

    request_data["AGGR_ID"] = Configuration.get_Property("ICICI_AGGR_ID")
    request_data["CrpId"] = cib_registration.corpId
    request_data["CrpUsr"] = cib_registration.userId
    request_data["BnfName"] = bene_data.get("full_name")
    request_data["BnfNickName"] = bene_data.get("full_name").split(" ")[0]
    # request_data["BnfNickName"] = "RakeshSourabhRT2Test11"
    request_data["BnfAccNo"] = bene_data.get("account_number")
    request_data["PayeeType"] = "W" if bene_data.get("bank").lower() == "icici" else "O"
    request_data["IFSC"] = bene_data.get("ifsc_code")
    request_data["URN"] = cib_registration.urn
    return {"status": True, "data": request_data}


def create_icici_bene_request_data_vpa(bene_data: dict) -> dict:
    request_data = {}

    merchant = bene_data.get("merchant")
    if merchant.default_account == "MERCHANT":
        cib_registration = CIBRegistration.objects.get(merchantId=bene_data['merchant_id'])
    elif merchant.default_account == "SABPAISA":
        cib_registration = CIBRegistration.objects.get(merchantId=getSabpaisaMerchantId())
    if not cib_registration:
        return {"status": False, "message": "Merchant is not registered with CIB"}

    request_data["aggrID"] = Configuration.get_Property("ICICI_AGGR_ID")
    request_data["corpID"] = cib_registration.corpId
    request_data["userID"] = cib_registration.userId
    request_data["urn"] = cib_registration.urn
    request_data["vpa"] = bene_data.get("upi_id")
    return {"status": True, "data": request_data}


def validate_bene_request_data(bene_data: dict) -> dict:
    bene_keys = ["full_name", "account_number", "ifsc_code", "bank"]
    for key in bene_keys:
        if not (key in bene_data and bene_data[key]):
            return {"status": False, "message": key + " is not provided"}

    name_validation_response = utils.validate_name(bene_data.get("full_name"))
    if not name_validation_response["status"]:
        return {"status": False, "message": name_validation_response["message"]}

    account_number_validation_response = utils.validate_account_number(bene_data.get("account_number"))
    if not account_number_validation_response["status"]:
        return {"status": False, "message": account_number_validation_response["message"]}

    # account_number_verification_response = utils.verify_account_number(bene_data.get("account_number"), bene_data.get("ifsc_code"), bene_data.get("merchant_id"))
    # if not account_number_verification_response["status"]:
    #     return {"status": False, "message": account_number_verification_response["message"]}

    return {"status": True, "message": "data is valid"}


def validate_upi_bene_request_data(bene_data) -> dict:
    bene_keys = ["full_name", "upi_id", "bank"]
    print("merchant id >> ", bene_data.get("merchant_id"))
    for key in bene_keys:
        if not (key in bene_data and bene_data[key]):
            return {"status": False, "message": key + " is not provided"}

    name_validation_response = utils.validate_name(bene_data.get("full_name"))
    if not name_validation_response["status"]:
        return {"status": False, "message": name_validation_response["message"]}

    upi_id_validation_response = utils.validate_upi_id(bene_data.get("upi_id"))
    if not upi_id_validation_response["status"]:
        return {"status": False, "message": upi_id_validation_response["message"]}

    # upi_id_verification_response = utils.verify_upi_id(bene_data.get("upi_id"), bene_data.get("merchant_id"))
    # if not upi_id_verification_response["status"]:
    #     return {"status": False, "message": upi_id_verification_response["message"]}

    return {"status": True, "message": "data is valid"}


def getSabpaisaMerchantId():
    return MerchantModel.objects.get(client_code="SABPAISA").id
