from apis.bank_services.ICICI_service import utils
from apis.bank_conf.config import Configuration
from datetime import date
import json


# key :  vpa value :  9540514993@paytm
# key :  mobile value :  9540514993
# key :  device_id value :  9540514993
# key :  seq_no value :  ICI50850823d71647a5a950e0a5d1a9be1a
# key :  account_provider value :  74
# key :  payee_va value :  9540514993@paytm
# key :  payer_va value :  9540514993@paytm
# key :  profile_id value :  56069237
# key :  amount value :  None
# key :  pre_approved value :  A
# key :  use_default_acc value :  D
# key :  default_debit value :  N
# key :  default_credit value :  N
# key :  payee_name value :  anand rathore
# key :  mcc value :  6011
# key :  merchant_type value :  ENTITY
# key :  txn_type value :  merchantToPersonPay
# key :  channel_code value :  MICICI
# key :  remarks value :  SALARY_DISBURSEMENT
# key :  crpID value :  PRACHICIB1
# key :  aggrID value :  CUST0589
# key :  userID value :  USER3
def createUpiStatusRequesData(data: dict) -> dict:
    request_data = {}
    if "date" not in data:
        request_data["date"] = date.today().strftime("%m/%d/%Y")
    request_data["mobile"] = data["mobile"]
    request_data["ori_seq_no"] = data["seq_no"]
    request_data["seq_no"] = utils.generate_seq_no()
    request_data["profile_id"] = data["profile_id"]
    request_data["device_id"] = data["device_id"]
    request_data["recon360"] = "N"
    request_data["channel_code"] = data["channel_code"]
    return utils.createPaymentRequestPayload(request_data)


def createImpsStatusRequesData(data: dict) -> dict:
    requests_data = {}
    if date not in data:
        requests_data["date"] = date.today().strftime("%m/%d/%Y")
    requests_data["transRefNo"] = data["tranRefNo"]
    requests_data["passCode"] = data["passCode"]
    requests_data["bcID"] = data["bcID"]
    requests_data["recon360"] = "N"
    return requests_data


def createNeftAndRtgsStatusRequestData(data: dict) -> dict:
    requests_data = {}
    requests_data["AGGRID"] = Configuration.get_Property("ICICI_AGGR_ID")
    requests_data["CORPID"] = data.get("crpId", data.get("CORPID"))
    requests_data["USERID"] = data.get("USERID", data.get("crpUsr"))
    requests_data["URN"] = data.get("URN", data.get("urn"))
    requests_data["UNIQUEID"] = data.get("UNIQUEID", data.get("tranRefNo"))
    return requests_data


def processICICIStatus(data: dict, headers: dict) -> dict:
    url = Configuration.get_Property("ICICI_Status")
    request_data = utils.create_icici_composite_request(data)
    response = utils.send_request(url=url, data=request_data, headers=headers)
    bank_data = {}
    try:
        bank_data = response.json()
        print("bank data : ", bank_data)
    except ValueError:
        print("Error in parsing the response from icici status service")
        bank_data["error"] = response.text
        print("bank data : ", bank_data)
    if 'encryptedKey' in bank_data:
        bank_data = json.loads(utils.decrypt_data(bank_data))
    return bank_data


# def processImpsStatus(data: dict, headers: dict) -> dict:
#     url = Configuration.get_Property("ICICI_Status")
#     print("========== Processing ICICI IMPS Status ==========")
#     request_data = utils.create_icici_composite_request(data)
#     response = utils.send_request(url=url, data=request_data, headers=headers)
#     bank_data = {}
#     try:
#         bank_data = response.json()
#         print("bank data : ", bank_data)
#     except ValueError:
#         print("Error in parsing the response from icici imps status service")
#         bank_data["error"] = response.text
#         print("bank data : ", bank_data)
#     if 'encryptedKey' in bank_data:
#         bank_data = json.loads(utils.decrypt_data(bank_data))
#     return bank_data


