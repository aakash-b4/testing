import json

from apis.bank_conf.config import Configuration
from apis.bank_models.ICICI_Model.payment_request_model import IciciUpiPaymentRequest
from apis.bank_services.ICICI_service import utils
from apis.database_models.CIBRegistrationModel import CIBRegistration
from apis.database_models.ClientModel import MerchantModel
from apis.database_models.IciciBeneficiaryModel import ICICI_Beneficiary
import logging

info_logger = logging.getLogger("info_logger")


def createIciciUpiRequestModel(map: dict):
    merchant = map["merchant"]
    # beneficiary = ICICI_Beneficiary.objects.get(upiId = map['upiId'])
    beneficiary = map.get("beneficiary")

    if not beneficiary:
        return {"status": False, "message": "Beneficiary does not exists"}

    if map.get("default_account") == "MERCHANT":
        cib_registration = CIBRegistration.objects.get(merchantId=map['merchant_id'])
    elif map.get("default_account") == "SABPAISA":
        cib_registration = CIBRegistration.objects.get(merchantId=getSabpaisaMerchantId())
    if not cib_registration:
        return {"status": False, "message": "Merchant is not registered with CIB"}

    icici_bene = ICICI_Beneficiary.objects.get(payout_beneficiary_id=beneficiary.id)

    map["mobile"] = merchant.phone
    map["device_id"] = merchant.phone
    map["seq_no"] = utils.generate_seq_no()
    map["account_provider"] = "74"
    map["payee_va"] = beneficiary.upi_id
    map["payer_va"] = merchant.upi_id
    map["profile_id"] = icici_bene.bnfId
    map["pre_approved"] = "P"
    map["use_default_acc"] = "D"
    map["default_debit"] = "N"
    map["default_credit"] = "N"
    map["payee_name"] = beneficiary.full_name
    map["mcc"] = "6011"
    map["merchant_type"] = "ENTITY"
    map["txn_type"] = "merchantToPersonPay"
    map["channel_code"] = "MICICI"
    map["remarks"] = map.get("none", "payment")
    map["crpID"] = cib_registration.corpId
    map["aggrID"] = Configuration.get_Property("ICICI_AGGR_ID")
    map["userID"] = cib_registration.userId
    map["vpa"] = merchant.upi_id
    iciciUpiPaymentRequest = IciciUpiPaymentRequest().from_Json(map)
    return {"status": True, "data": iciciUpiPaymentRequest}


def processIciciPayment(requestModel: IciciUpiPaymentRequest, headers: dict) -> dict:
    print("========= Processing icici payment =========")
    json_request_model = requestModel.to_Json()
    json_request_modoel = utils.createPaymentRequestPayload(json_request_model)
    json_request_model = utils.create_icici_composite_request(json_request_modoel)
    url = Configuration.get_Property("ICICI_PaymentURL")
    # response = utils.send_request(url=url, data=json_request_model, headers=headers)
    bank_data = {}
    try:
        # bank_data = response.json()
        print("bank data : ", bank_data)
    except ValueError:
        # bank_data["except_error"] = response.text
        bank_data["success"] = False
        print("bank data in exception: ", bank_data)
    if 'encryptedKey' in bank_data:
        bank_data = json.loads(utils.decrypt_data(bank_data))
    return bank_data


def processIciciAnotherPayment(requestModel: dict, headers: dict) -> dict:
    print("========= Processing icici payment =========")
    json_request_model = utils.create_icici_composite_request(requestModel)
    url = Configuration.get_Property("ICICI_PaymentURL")
    # response = utils.send_request(url=url, data=json_request_model, headers=headers)
    bank_data = {}
    try:
        # bank_data = response.json()
        print("bank data : ", bank_data)
    except ValueError:
        # bank_data["except_error"] = response.text
        bank_data["success"] = False
        print("bank data in exception: ", bank_data)
    if 'encryptedKey' in bank_data:
        bank_data = json.loads(utils.decrypt_data(bank_data))
    return bank_data


def getUpiHeader():
    return {"x-priority": "1000"}


def getImpsHeader():
    return {"x-priority": "0100"}


def getNeftHeader():
    return {"x-priority": "0010"}


def getRtgsHeader():
    return {"x-priority": "0001"}


def getSabpaisaMerchantId():
    return MerchantModel.objects.get(client_code="SABPAISA").id


def createIciciImpsRequestModel(map):
    new_map = {}
    beneficiary = map.get("beneficiary")
    merchant = map.get("merchant")
    if map.get("default_account") == "MERCHANT":
        cib_registration = CIBRegistration.objects.get(merchantId=map['merchant_id'])
    elif map.get("default_account") == "SABPAISA":
        cib_registration = CIBRegistration.objects.get(merchantId=getSabpaisaMerchantId())
    if not cib_registration:
        return {"status": False, "message": "Merchant is not registered with CIB"}

    new_map["aggrId"] = Configuration.get_Property("ICICI_AGGR_ID")
    new_map["crpUsr"] = cib_registration.userId
    new_map["mobile"] = merchant.phone
    new_map["crpId"] = cib_registration.corpId
    new_map["bcID"] = map.get("bcID", "IBCKer00055")
    new_map["passCode"] = map.get("passCode", "447c4524c9074b8c97e3a3c40ca7458d")
    new_map["retailerCode"] = map.get("retailerCode", "rcode")
    new_map["senderName"] = merchant.client_name
    new_map["paymentRef"] = "FTTransfer" + utils.generate_order_id().upper()
    new_map["tranRefNo"] = utils.generate_order_id()
    new_map["amount"] = map.get("amount", "1.00")
    new_map["beneIFSC"] = beneficiary.ifsc_code
    new_map["beneAccNo"] = beneficiary.account_number
    new_map["localTxnDtTime"] = utils.get_concatenated_local_date()
    return {"status": True, "data": new_map}


def createIciciNeftRequestModel(map):
    new_map = {}
    beneficiary = map.get("beneficiary")
    merchant = map.get("merchant")
    if map.get("default_account") == "MERCHANT":
        cib_registration = CIBRegistration.objects.get(merchantId=map['merchant_id'])
    elif map.get("default_account") == "SABPAISA":
        cib_registration = CIBRegistration.objects.get(merchantId=getSabpaisaMerchantId())
    if not cib_registration:
        return {"status": False, "message": "Merchant is not registered with CIB"}

    new_map["tranRefNo"] = utils.generate_order_id()
    new_map["crpId"] = cib_registration.corpId
    new_map["aggrId"] = Configuration.get_Property("ICICI_AGGR_ID")
    new_map["crpUsr"] = cib_registration.userId
    new_map["aggrName"] = Configuration.get_Property("ICICI_AGGR_NAME")
    new_map["amount"] = map.get("amount").split(".")[0]
    new_map["senderAcctNo"] = merchant.account_number
    new_map["beneAccNo"] = beneficiary.account_number
    new_map["beneName"] = beneficiary.full_name
    new_map["beneIFSC"] = beneficiary.ifsc_code
    new_map["narration1"] = map.get("purpose", "N/A")
    new_map["urn"] = cib_registration.urn
    new_map["txnType"] = map.get("txnType", "RGS")
    new_map["WORKFLOW_REQD"] = map.get("WORKFLOW_REQD", "N")
    return {"status": True, "data": new_map}


def createIciciRtgsRequestModel(map):
    new_map = {}
    beneficiary = map.get("beneficiary")
    merchant = map.get("merchant")
    if map.get("default_account") == "MERCHANT":
        cib_registration = CIBRegistration.objects.get(merchantId=map['merchant_id'])
    elif map.get("default_account") == "SABPAISA":
        cib_registration = CIBRegistration.objects.get(merchantId=getSabpaisaMerchantId())
    if not cib_registration:
        return {"status": False, "message": "Merchant is not registered with CIB"}

    new_map["CORPID"] = cib_registration.corpId
    new_map["AGGRID"] = Configuration.get_Property("ICICI_AGGR_ID")
    new_map["USERID"] = cib_registration.userId
    new_map["URN"] = cib_registration.urn
    new_map["AGGRNAME"] = Configuration.get_Property("ICICI_AGGR_NAME")
    new_map["UNIQUEID"] = utils.generate_order_id()
    new_map["DEBITACC"] = merchant.account_number
    new_map["CREDITACC"] = beneficiary.account_number
    new_map["IFSC"] = beneficiary.ifsc_code
    new_map["AMOUNT"] = map.get("amount")
    new_map["CURRENCY"] = "INR"
    new_map["TXNTYPE"] = "TPA"
    new_map["PAYEENAME"] = beneficiary.full_name
    new_map["REMARKS"] = map.get("purpose", "N/A")
    new_map["WORKFLOW_REQD"] = "N"
    return {"status": True, "data": new_map}


def validate_upi_request(upi_request_data: dict) -> dict:
    upi_keys = ["orderId", "upiId", "amount", "purpose"]
    for key in upi_keys:
        if not (key in upi_request_data and upi_request_data[key]):
            return {"status": False, "message": key + " is not provided"}

    upi_id_validation_response = utils.validate_upi_id(upi_request_data.get("upiId"))
    if not upi_id_validation_response["status"]:
        return {"status": False, "message": upi_id_validation_response["message"]}

    order_id_validation_response = utils.validate_order_id(upi_request_data.get("orderId"))
    if not order_id_validation_response["status"]:
        return {"status": False, "message": order_id_validation_response["message"]}

    amount_validation_response = utils.validate_amount(upi_request_data.get("amount"))
    if not amount_validation_response["status"]:
        return {"status": False, "message": amount_validation_response["message"]}

    return {"status": True, "data": "upi request data is valid"}

def validate_neft_imps_rtgs_request(neft_imps_rtgs_request_data: dict) -> dict:
    neft_keys = ["orderId", "beneficiaryAccount", "beneficiaryIFSC", "amount"]
    for key in neft_keys:
        if not (key in neft_imps_rtgs_request_data and neft_imps_rtgs_request_data[key]):
            return {"status": False, "message": key + " is not provided"}

    beneficiaryAccount_validation_response = utils.validate_account_number(neft_imps_rtgs_request_data.get("beneficiaryAccount"))
    if not beneficiaryAccount_validation_response["status"]:
        return {"status": False, "message": beneficiaryAccount_validation_response["message"]}

    order_id_validation_response = utils.validate_order_id(neft_imps_rtgs_request_data.get("orderId"))
    if not order_id_validation_response["status"]:
        return {"status": False, "message": order_id_validation_response["message"]}

    amount_validation_response = utils.validate_amount(neft_imps_rtgs_request_data.get("amount"))
    if not amount_validation_response["status"]:
        return {"status": False, "message": amount_validation_response["message"]}

    ifsc_validation_response = utils.validate_amount(neft_imps_rtgs_request_data.get("beneficiaryIFSC"))
    if not amount_validation_response["status"]:
        return {"status": False, "message": ifsc_validation_response["message"]}    

    return {"status": True, "data": "Request data is valid"}    
