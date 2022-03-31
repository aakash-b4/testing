import json
import threading
import time
from datetime import datetime

import requests

import paytmchecksum
from apis.bank_services.ICICI_service import paymentService as icici_payment_service
from apis.bank_services.ICICI_service import statusService as iciciStatusService
from apis.bank_services.ICICI_service import utils as icici_utils
from apis.database_service.Charge_breaking_model_services import Charge_Breaking_model_services
from apis.database_service.Webhook_Request_model_service import Webhook_Request_Model_Service
from sabpaisa import auth
from .. import const
from ..RequestModels.payoutrequestmodel import PayoutRequestModel
from ..Utils import generater
from ..Utils import splitString
from ..Utils import statuscodes
from ..bank_models.PAYTM_Model import payment_request_model as paytm_request_model
from ..bank_models.PAYTM_Model import payment_response_model as paytm_response_model
from ..database_service import Client_model_service, Ledger_model_services, Mode_model_services, \
    Beneficiary_model_services, Slab_model_services
from ..database_service.Log_model_services import Log_Model_Service
from ..database_service.Webhook_model_service import Webhook_Model_Service
import logging

logger = logging.getLogger("logger")


class PayoutService:
    def __init__(self, merchant_id=None, encrypted_code=None, client_ip_address=None):
        self.merchant_id = merchant_id
        self.client_ip_address = client_ip_address
        self.encrypted_code = encrypted_code

    def excutePAYTM(self, mode_rec):

        log = Log_Model_Service(log_type="excuting PAYTM service", client_ip_address=self.client_ip_address,
                                server_ip_address=const.server_ip, created_by=self.merchant_id)
        log.save()
        try:
            clientModelService = Client_model_service.Client_Model_Service()
            clientModel = clientModelService.fetch_by_id(
                self.merchant_id, self.client_ip_address, "Merchant_Id ::" + str(self.merchant_id))
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            # auth_token = req.headers["auth_token"]
            # merchant_id= auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            # merchant=MerchantModel.objects.get(id=self.merchant_id)
            # role = RoleModel.objects.get(id=merchant.role)
            query = self.encrypted_code
            if clientModel.is_encrypt:
                query = auth.AESCipher(authKey, authIV).decrypt(
                    self.encrypted_code)
            print("query", query)
            map = splitString.StringToMap(query)
            map["mode"] = mode_rec
            # if map["usern"]!=clientModel.client_username and map["pass"]!=clientModel.client_password:
            #     return [False,{}]
            payoutrequestmodel, valid, message = PayoutRequestModel.from_json(
                map)
            # print('upiid :: '+payoutrequestmodel.upiId)
            print("valid :: " + str(valid))
            # print(payoutrequestmodel.clientPaymode)
            mode = Mode_model_services.Mode_Model_Service.fetch_by_mode(
                payoutrequestmodel.mode)
            if valid:
                bal = Ledger_model_services.Ledger_Model_Service.getBalance(
                    self.merchant_id, self.client_ip_address, "Merchant_ID :: " + str(self.merchant_id))
                print("amount :: " + payoutrequestmodel.amount)
                print("balance ::" + str(bal))
                log = Log_Model_Service(json=str({"merchant_id": self.merchant_id}),
                                        log_type="Checking for duplicate order id",
                                        client_ip_address=self.client_ip_address,
                                        server_ip_address=const.server_ip,
                                        remarks="checking for duplicate order id for merchant id :: " + self.merchant_id + " orderid :: " + str(
                                            payoutrequestmodel.orderId))
                log.save()
                check_cus = Ledger_model_services.Ledger_Model_Service.fetch_by_customer_ref_no(
                    self.merchant_id, payoutrequestmodel.orderId)
                if check_cus is None:
                    return ["Duplicate Order id", {}, False]
                if bal < float(payoutrequestmodel.amount):
                    return ["Not Sufficent Balance", {}, False]
                if mode_rec == "UPI":
                    bene = Beneficiary_model_services.Beneficiary_Model_Services.fetch_by_upiId(
                        self.merchant_id, payoutrequestmodel.upiId)
                else:
                    bene = Beneficiary_model_services.Beneficiary_Model_Services.fetch_by_account_number_ifsc(
                        self.merchant_id, payoutrequestmodel.beneficiaryAccount, payoutrequestmodel.beneficiaryIFSC)

                if bene == None:
                    return ["Beneficiary Not Added", {}, False]
                if not Slab_model_services.Slab_Model_Service.check_slab(self.merchant_id, payoutrequestmodel.amount):
                    return ["Cannot proccess this volume of amount", {}, False]
                ledgerModelService = Ledger_model_services.Ledger_Model_Service()
                clientModelService = Client_model_service.Client_Model_Service()
                clientmodel = clientModelService.fetch_by_id(
                    self.merchant_id, self.client_ip_address, "Merchant Id ::" + str(self.merchant_id))
                ledgerModelService.client_id = clientModel.id
                ledgerModelService.merchant = self.merchant_id
                ledgerModelService.client_code = clientModel.client_code
                ledgerModelService.amount = payoutrequestmodel.amount
                ledgerModelService.bank_id = clientmodel.bank_id
                ledgerModelService.bank_ref_no = "null"

                ledgerModelService.customer_ref_no = payoutrequestmodel.orderId
                ledgerModelService.trans_status = "Initiated"
                if mode_rec != "UPI":
                    print("if ledger")
                    ledgerModelService.bene_account_name = payoutrequestmodel.beneficiaryName
                    ledgerModelService.bene_account_number = payoutrequestmodel.beneficiaryAccount
                    ledgerModelService.bene_ifsc = payoutrequestmodel.beneficiaryIFSC
                else:
                    print("else ledger")
                    ledgerModelService.upiId = payoutrequestmodel.upiId
                ledgerModelService.request_header = "null"
                ledgerModelService.type_status = "Generated"
                ledgerModelService.trans_type = "payout"

                #  order_id=paytm_extra.generate_order_id()
                #  ledgerModelService.customer_ref_no=order_id

                charge = Ledger_model_services.Ledger_Model_Service.calculate_charge(
                    self.merchant_id, mode_rec, payoutrequestmodel.amount, self.client_ip_address)
                print("charges :: " + str(charge))
                if charge == [0, 0]:
                    return ["charges not added to this mode", {}, False]

                taxes = Ledger_model_services.Ledger_Model_Service.calculate_tax(
                    clientModel.is_tax_inclusive, [ls for ls in charge[1]])

                print("charge :: " + str(charge))
                ledgerModelService.charge = taxes[2]
                ledgerModelService.van = "null"
                ledgerModelService.status_code = statuscodes.statuscodes["Initiated"]
                ledgerModelService.mode = mode.id
                ledgerModelService.purpose = payoutrequestmodel.purpose
                ledgerModelService.is_tax_inclusive = clientModel.is_tax_inclusive
                ledgerModelService.tax = taxes[0]
                ledgerModelService.payout_trans_id = generater.generate_token()
                ledgerModelService.trans_amount_type = "dr"
                ledgerModelService.trans_time = datetime.now()
                ledgerModelService.total_amount = float(
                    ledgerModelService.amount) + float(ledgerModelService.charge) + float(ledgerModelService.tax)
                id = ledgerModelService.save(
                    client_ip_address=self.client_ip_address, createdBy="Merchant Id :: " + str(self.merchant_id))
                ledgerModelService.update_status(
                    id, 'Requested', client_ip_address=self.client_ip_address,
                    created_by="Merchant_Id :: " + str(self.merchant_id))
                ledger_id = id
                tax_charges = Charge_Breaking_model_services(
                    charge_amount=taxes[0], charge_id=0, transaction_id=ledger_id,
                    payout_transaction_id=ledgerModelService.payout_trans_id, tax_amount=0, charge_type="tax")
                tax_charges.save()
                #  tax_ledger=Ledger_model_services.Ledger_Model_Service()
                #  tax_ledger.client_id=clientModel.id
                #  tax_ledger.merchant=self.merchant_id
                #  tax_ledger.client_code=clientModel.client_code
                #  tax_ledger.amount=taxes[0]
                #  tax_ledger.bank_id=clientmodel.bank_id
                #  tax_ledger.bank_ref_no="null"
                #  tax_ledger.customer_ref_no=payoutrequestmodel.orderId
                #  tax_ledger.trans_status="Pending"
                #  if mode_rec!="UPI":
                #     print("if ledger")
                #     tax_ledger.bene_account_name=payoutrequestmodel.beneficiaryName
                #     tax_ledger.bene_account_number=payoutrequestmodel.beneficiaryAccount
                #     tax_ledger.bene_ifsc=payoutrequestmodel.beneficiaryIFSC
                #  else:
                #      print("else ledger")
                #      tax_ledger.upiId=payoutrequestmodel.upiId
                #  tax_ledger.type_status="Generated"
                #  tax_ledger.trans_type="tax"
                #  tax_ledger.request_header="null"
                #  tax_ledger.mode=mode.id
                #  tax_ledger.van=""
                #  tax_ledger.charge=0
                #  tax_ledger.tax=0
                #  tax_ledger.is_tax_inclusive=ledgerModelService.is_tax_inclusive
                #  tax_ledger.linked_ledger_id=ledgerModelService.payout_trans_id
                #  tax_ledger.payout_trans_id=generater.generate_token()
                #  tax_ledger.trans_amount_type = "dr"
                #  tax_ledger.charge_id=0
                #  #  ledgerModelService.
                #  tax_ledger.trans_time=datetime.now()
                #  tax_ledger.save("Merchant Id :: "+str(self.merchant_id),self.client_ip_address)
                irt = 0
                for i in charge[1]:
                    print(i)
                    charge_ledger = Charge_Breaking_model_services(
                        charge_amount=i[0], charge_id=taxes[1][irt][0], transaction_id=ledger_id,
                        payout_transaction_id=ledgerModelService.payout_trans_id, tax_amount=taxes[1][irt][1],
                        charge_type="charge")
                    charge_ledger.save()
                    # charge_ledger=Ledger_model_services.Ledger_Model_Service()
                    # charge_ledger.client_id=clientModel.id
                    # charge_ledger.merchant=self.merchant_id
                    # charge_ledger.client_code=clientModel.client_code
                    # charge_ledger.amount=i[0]
                    # charge_ledger.bank_id=clientmodel.bank_id
                    # charge_ledger.bank_ref_no="null"
                    # charge_ledger.customer_ref_no=payoutrequestmodel.orderId
                    # charge_ledger.trans_status="Pending"
                    # if mode_rec!="UPI":
                    #     print("if ledger")
                    #     charge_ledger.bene_account_name=payoutrequestmodel.beneficiaryName
                    #     charge_ledger.bene_account_number=payoutrequestmodel.beneficiaryAccount
                    #     charge_ledger.bene_ifsc=payoutrequestmodel.beneficiaryIFSC
                    # else:
                    #     print("else ledger")
                    #     charge_ledger.upiId=payoutrequestmodel.upiId
                    # charge_ledger.type_status="Generated"
                    # charge_ledger.trans_type="charge"
                    # charge_ledger.request_header="null"
                    # charge_ledger.mode=mode.id
                    # charge_ledger.van=""
                    # charge_ledger.charge=0
                    # charge_ledger.tax=taxes[1][irt][1]
                    # charge_ledger.is_tax_inclusive=ledgerModelService.is_tax_inclusive
                    # charge_ledger.linked_ledger_id=ledgerModelService.payout_trans_id
                    # charge_ledger.payout_trans_id=generater.generate_token()
                    # charge_ledger.trans_amount_type = "dr"
                    # charge_ledger.charge_id=taxes[1][irt][0]
                    # #  ledgerModelService.
                    # charge_ledger.trans_time=datetime.now()
                    # charge_ledger.save("Merchant Id :: "+str(self.merchant_id),self.client_ip_address)

                    irt += 1
                if mode_rec == "UPI":
                    request_model = paytm_request_model.Payment_Request_Model(transfer_mode=payoutrequestmodel.mode,
                                                                              subwalletGuid=const.paytm_subwalletGuid,
                                                                              orderId=ledgerModelService.payout_trans_id,
                                                                              beneficiaryVPA=payoutrequestmodel.upiId,
                                                                              amount=payoutrequestmodel.amount,
                                                                              purpose="OTHERS")

                else:
                    request_model = paytm_request_model.Payment_Request_Model(
                        beneficiaryName=payoutrequestmodel.beneficiaryName, transfer_mode=payoutrequestmodel.mode,
                        subwalletGuid=const.paytm_subwalletGuid,
                        orderId=ledgerModelService.payout_trans_id,
                        beneficiaryAccount=payoutrequestmodel.beneficiaryAccount,
                        beneficiaryIFSC=payoutrequestmodel.beneficiaryIFSC, amount=payoutrequestmodel.amount,
                        purpose="OTHERS")

                log_model = Log_Model_Service(json=str({"merchant_id": self.merchant_id}), log_type="Paytm_Request",
                                              server_ip_address=const.server_ip,
                                              client_ip_address=self.client_ip_address,
                                              full_request=str(request_model.to_json()))
                log_id = log_model.save()
                post_data = json.dumps(request_model.to_json())
                checksum = paytmchecksum.generateSignature(
                    post_data, const.paytm_merchant_key)

                response = requests.post(const.paytm_link_transaction, json=request_model.to_json(), headers={
                    "Content-type": "application/json", "x-mid": const.paytm_merchant_id, "x-checksum": checksum})
                print(response.json())
                Log_Model_Service.update_response(
                    log_id, response=str(response.json()))
                response_model = paytm_response_model.Payment_Response_Model.from_json(
                    response.json())
                client_ip_address_temp = self.client_ip_address
                merchant_id_temp = self.merchant_id

                class ServiceThread2(threading.Thread):
                    def run(self):
                        log = Log_Model_Service(json=str({"merchant_id": merchant_id_temp}), log_type="Thread",
                                                client_ip_address=client_ip_address_temp,
                                                server_ip_address=const.server_ip,
                                                remarks="Running service thread on webhook apis for merchant id :: " + merchant_id_temp)
                        log.save()
                        transhistory = Ledger_model_services.Ledger_Model_Service.fetch_by_id(
                            id=ledger_id, client_ip_address=client_ip_address_temp, created_by="system")

                        webhookrequest = Webhook_Request_Model_Service()
                        webhookrequest.payout_trans_id = transhistory.payout_trans_id
                        webhookrequest.hit_init_time = datetime.now()
                        webhookrequest.status = False
                        id = webhookrequest.save()

                        webhooks = Webhook_Model_Service.fetch_by_merchant_id_payout(
                            merchant_id_temp, client_ip_address_temp)
                        print("Webhook Started at :: " + str(webhooks.webhook))
                        if webhooks is not None and not webhooks.is_instant:
                            print("Interval Webhook :: " +
                                  str(webhooks.time_interval) + " min ")
                            interval = webhooks.time_interval
                            time.sleep(60 * interval)
                        if webhooks is None:
                            pass
                        else:

                            transhistoryJson = Ledger_model_services.Ledger_Model_Service.fetch_by_id_tojson(
                                id=ledger_id, client_ip_address=client_ip_address_temp, created_by="system")
                            response = requests.post(
                                webhooks.webhook, json=transhistoryJson)
                            print("First Response from webhook :: " + response.text)
                            if response.status_code != 200:
                                for i in range(webhooks.max_request):
                                    interval = webhooks.time_interval
                                    time.sleep(60 * interval)
                                    response = requests.post(
                                        webhooks.webhook, json=transhistoryJson)
                                    print(
                                        str(i) + "th response from webhook :: " + response.text)
                                    if response.status_code == 200:
                                        break
                            if response.status_code == 200:
                                print("updating response as true")
                                Webhook_Request_Model_Service.update_webhook(
                                    id, True, response.text)
                            else:
                                print("updating response as false")
                                Webhook_Request_Model_Service.update_webhook(
                                    id, False, response.text)

                if response_model.status == "ACCEPTED":
                    ledgerModelService.update_status(
                        id, "Proccesing", client_ip_address=self.client_ip_address,
                        created_by="Merchant ID :: " + str(self.merchant_id))
                    client_ip_address_temp = self.client_ip_address
                    merchant_id_temp = self.merchant_id
                    thread = None

                    class ServiceThread(threading.Thread):
                        def run(self):
                            log = Log_Model_Service(json=str({"merchant_id": merchant_id_temp}), log_type="Thread",
                                                    full_request={"orderId": ledgerModelService.payout_trans_id},
                                                    client_ip_address=client_ip_address_temp,
                                                    server_ip_address=const.server_ip,
                                                    remarks="Running service thread on paytm enquiry api for merchant id :: " + merchant_id_temp)
                            logid = log.save()
                            time.sleep(40)
                            checksum = paytmchecksum.generateSignature(json.dumps(
                                {"orderId": ledgerModelService.payout_trans_id}), const.paytm_merchant_key)
                            response = requests.post(const.paytm_link_enquiry,
                                                     json={"orderId": ledgerModelService.payout_trans_id}, headers={
                                    "Content-type": "application/json",
                                    "x-mid": const.paytm_merchant_id,
                                    "x-checksum": checksum})
                            log.update_response(logid, response.text)
                            print(response.json())
                            if response.json()['status'] == "SUCCESS":
                                ledgerModelService.update_status(id, "Success", client_ip_address_temp,
                                                                 "Merchant :: " + str(
                                                                     merchant_id_temp),
                                                                 response.json()['result']['rrn'])
                                ledgerModelService.update_trans_time(id, datetime.now(
                                ), client_ip_address_temp, "Merchant :: " + str(merchant_id_temp))
                            #  charge = Ledger_model_services.Ledger_Model_Service.fetch_by_linked_id(ledgerModelService.payout_trans_id)
                            #  if clientModel.is_charge:

                            #     for i in charge:
                            #         ledgerModelService.update_status(i.id,"Success",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                            #  else:
                            #      for i in charge:
                            #         ledgerModelService.update_status(i.id,"Failed",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))

                            elif response.json()["status"] == "PENDING":
                                ledgerModelService.update_status(
                                    id, "Pending", client_ip_address_temp, "Merchant :: " + str(merchant_id_temp))

                                ServiceThread().start()
                            else:
                                #  charge = Ledger_model_services.Ledger_Model_Service.fetch_by_linked_id(ledgerModelService.payout_trans_id)
                                #  for i in charge:
                                #         ledgerModelService.update_status(i.id,"Failed",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))

                                ledgerModelService.update_status(
                                    id, "Failed", client_ip_address_temp, "Merchant :: " + str(merchant_id_temp))
                            print("Service Done")

                    thread = ServiceThread().start()

                else:
                    #  charge = Ledger_model_services.Ledger_Model_Service.fetch_by_linked_id(ledgerModelService.payout_trans_id)
                    #  for i in charge:
                    #                     ledgerModelService.update_status(i.id,"Failed",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))

                    ledgerModelService.update_status(
                        id, "Failed", self.client_ip_address, "Merchant :: " + str(self.merchant_id))
                thread2 = ServiceThread2().start()

                return ["Payout Done",
                        {"orderId": ledgerModelService.customer_ref_no, "amount": ledgerModelService.amount,
                         "status": "PROCESSING", "requestedDatetime": str(datetime.now()).split(".")[0]}, True]

            else:
                return [message, {}, False]
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(e.args)
            return [e.args, {}, False]

    def excuteICICI(self, mode_rec):
        global bal
        log = Log_Model_Service(json=str({"merchant_id": self.merchant_id}), log_type="excuting ICICI payment service",
                                client_ip_address=self.client_ip_address, server_ip_address=const.server_ip,
                                created_by=self.merchant_id)
        log.save()
        try:
            clientModelService = Client_model_service.Client_Model_Service()
            # clientModel = clientModelService.fetch_by_clientcode(
            #     self.client_code)
            clientModel = clientModelService.fetch_by_id(
                self.merchant_id, self.client_ip_address, "Merchant Id ::" + str(self.merchant_id))

            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            query = auth.AESCipher(authKey, authIV).decrypt(
                self.encrypted_code)
            logger.info("query " + query)
            map = splitString.StringToMap(query)
            logger.info("map " + str(map))

            if mode_rec.lower() == "upi":
                upi_validation_response = icici_payment_service.validate_upi_request(map)
                if not upi_validation_response["status"]:
                    return [upi_validation_response["message"], {}, False]

            if mode_rec.lower() in ("neft", "imps", "rtgs"):
                neft_imps_rtgs_validation_response = icici_payment_service.validate_neft_imps_rtgs_request(map)
                if not neft_imps_rtgs_validation_response["status"]:
                    return [neft_imps_rtgs_validation_response["message"], {}, False]

            logger.info("amount === " + map["amount"])
            map["mode"] = mode_rec
            payoutrequestmodel, valid, message = PayoutRequestModel.from_json(
                map)
            mode = Mode_model_services.Mode_Model_Service.fetch_by_mode(
                payoutrequestmodel.mode)
            if valid:
                map["default_account"] = clientModel.default_account
                if clientModel.default_account == "SABPAISA":
                    bal = Ledger_model_services.Ledger_Model_Service.getBalance(
                        self.merchant_id, self.client_ip_address, "Merchant_ID :: " + str(self.merchant_id))
                    if bal < float(payoutrequestmodel.amount):
                        return "Not Sufficient Balance"
                check_cus = Ledger_model_services.Ledger_Model_Service.fetch_by_customer_ref_no(
                    self.merchant_id, payoutrequestmodel.orderId)
                if check_cus is None:
                    return ["Duplicate Order id", {}, False]
                if mode_rec == "UPI":
                    bene = Beneficiary_model_services.Beneficiary_Model_Services.fetch_by_upiId(
                        self.merchant_id, payoutrequestmodel.upiId)
                else:
                    bene = Beneficiary_model_services.Beneficiary_Model_Services.fetch_by_account_number_ifsc(
                        self.merchant_id, payoutrequestmodel.beneficiaryAccount, payoutrequestmodel.beneficiaryIFSC)[0]

                if bene is None:
                    return ["Beneficiary Not Added", {}, False]

                if "beneficiaryName" in map:
                    if bene.full_name != map["beneficiaryName"]:
                        return ["Beneficiary Name Does Not Match", {}, False]

                if not Slab_model_services.Slab_Model_Service.check_slab(self.merchant_id, payoutrequestmodel.amount):
                    return ["Cannot process this volume of amount", {}, False]
                ledgerModelService = Ledger_model_services.Ledger_Model_Service()
                clientModelService = Client_model_service.Client_Model_Service()
                # clientmodel = clientModelService.fetch_by_clientcode(
                #     self.client_code)
                clientmodel = clientModelService.fetch_by_id(
                    self.merchant_id, self.client_ip_address, "Merchant Id ::" + str(self.merchant_id))
                ledgerModelService.client_id = clientModel.id
                ledgerModelService.merchant = self.merchant_id
                ledgerModelService.client_code = clientModel.client_code
                ledgerModelService.amount = payoutrequestmodel.amount
                ledgerModelService.bank_id = clientmodel.bank_id
                ledgerModelService.bank_ref_no = "null"

                ledgerModelService.customer_ref_no = payoutrequestmodel.orderId
                ledgerModelService.trans_status = "Initiated"
                if mode_rec.upper() != "UPI":
                    print("if ledger")
                    ledgerModelService.bene_account_name = payoutrequestmodel.beneficiaryName
                    ledgerModelService.bene_account_number = payoutrequestmodel.beneficiaryAccount
                    ledgerModelService.bene_ifsc = payoutrequestmodel.beneficiaryIFSC
                else:
                    print("else ledger")
                    ledgerModelService.upiId = payoutrequestmodel.upiId

                ledgerModelService.request_header = "null"
                ledgerModelService.type_status = "Generated"
                ledgerModelService.trans_type = "payout"

                charge = Ledger_model_services.Ledger_Model_Service.calculate_charge(
                    self.merchant_id, mode_rec, payoutrequestmodel.amount, self.client_ip_address)
                print("charges :: " + str(charge))
                if charge == [0, 0]:
                    return ["charges not added to this mode", {}, False]

                taxes = Ledger_model_services.Ledger_Model_Service.calculate_tax(
                    clientModel.is_tax_inclusive, [ls for ls in charge[1]])

                print("charge :: " + str(charge))
                ledgerModelService.charge = taxes[2]
                ledgerModelService.van = "null"
                ledgerModelService.status_code = statuscodes.statuscodes["Initiated"]
                ledgerModelService.mode = mode.id
                ledgerModelService.purpose = payoutrequestmodel.purpose
                ledgerModelService.is_tax_inclusive = clientModel.is_tax_inclusive
                ledgerModelService.tax = taxes[0]
                ledgerModelService.payout_trans_id = generater.generate_token()
                ledgerModelService.trans_amount_type = "dr"
                ledgerModelService.trans_time = datetime.now()
                ledgerModelService.total_amount = float(
                    ledgerModelService.amount) + float(ledgerModelService.charge) + float(ledgerModelService.tax)
                id = ledgerModelService.save(
                    client_ip_address=self.client_ip_address, createdBy="Merchant Id :: " + str(self.merchant_id))
                ledgerModelService.update_status(
                    id, 'Requested', client_ip_address=self.client_ip_address,
                    created_by="Merchant_Id :: " + str(self.merchant_id))
                ledger_id = id
                tax_charges = Charge_Breaking_model_services(
                    charge_amount=taxes[0], charge_id=0, transaction_id=ledger_id,
                    payout_transaction_id=ledgerModelService.payout_trans_id, tax_amount=0, charge_type="tax")
                tax_charges.save()

                irt = 0
                for i in charge[1]:
                    print(i)
                    charge_ledger = Charge_Breaking_model_services(
                        charge_amount=i[0], charge_id=taxes[1][irt][0], transaction_id=ledger_id,
                        payout_transaction_id=ledgerModelService.payout_trans_id, tax_amount=taxes[1][irt][1],
                        charge_type="charge")
                    charge_ledger.save()
                    irt += 1
                # ====================================================================

                map["merchant"] = clientModel
                map["beneficiary"] = bene
                if mode_rec.lower() == "upi":
                    header = icici_payment_service.getUpiHeader()
                    iciciPaymentRequestModel = icici_payment_service.createIciciUpiRequestModel(map)
                    if not iciciPaymentRequestModel.get("status"):
                        return iciciPaymentRequestModel.get("message", iciciPaymentRequestModel.get("message"))
                    response = icici_payment_service.processIciciPayment(iciciPaymentRequestModel.get("data"), header)

                elif mode_rec.lower() == "imps":
                    header = icici_payment_service.getImpsHeader()
                    iciciPaymentRequestModel = icici_payment_service.createIciciImpsRequestModel(map)
                    if not iciciPaymentRequestModel.get("status"):
                        return iciciPaymentRequestModel.get("message", iciciPaymentRequestModel.get("message"))
                    response = icici_payment_service.processIciciAnotherPayment(iciciPaymentRequestModel.get("data"),
                                                                                header)
                elif mode_rec.lower() == "neft":
                    header = icici_payment_service.getNeftHeader()
                    iciciPaymentRequestModel = icici_payment_service.createIciciNeftRequestModel(map)
                    if not iciciPaymentRequestModel.get("status"):
                        return iciciPaymentRequestModel.get("message", iciciPaymentRequestModel.get("message"))
                    response = icici_payment_service.processIciciAnotherPayment(iciciPaymentRequestModel.get("data"),
                                                                                header)
                elif mode_rec.lower() == "rtgs":
                    header = icici_payment_service.getRtgsHeader()
                    iciciPaymentRequestModel = icici_payment_service.createIciciRtgsRequestModel(map)
                    if not iciciPaymentRequestModel.get("status"):
                        return iciciPaymentRequestModel.get("message", iciciPaymentRequestModel.get("message"))
                    response = icici_payment_service.processIciciAnotherPayment(iciciPaymentRequestModel.get("data"),
                                                                                header)
                    logger.info("response >> ", response)
                else:
                    return "Invalid Payment Mode"

                log_model = Log_Model_Service(json=str({"merchant_id": self.merchant_id}),
                                              log_type="ICICI_Payment_Request",
                                              server_ip_address=const.server_ip,
                                              client_ip_address=self.client_ip_address,
                                              full_request=iciciPaymentRequestModel.get("data"))

                log_id = log_model.save()
                Log_Model_Service.update_response(log_id, response=response)
                if mode_rec.lower() == "upi":
                    resp = response.get("response", "0")
                    message = response.get("message", "Transaction Successful")
                    UpiTranlogId = response.get("UpiTranlogId", icici_utils.generate_random_number())
                    UserProfile = response.get("userProfile", icici_utils.generate_random_number())
                    SeqNo = response.get("SeqNo", iciciPaymentRequestModel.get("data").get("seq_no"))
                    MobileAppData = response.get("MoblieAppData", "SUCCESS")
                    PayerRespCode = response.get("PayerRespCode", "00")
                    BankRRN = response.get("BankRRN", icici_utils.generate_random_number())
                    if resp == "0" and message == "Transaction Successful":
                        logger.info("===== ICICI UPI payment success =====")
                        status = "Success"
                    else:
                        logger.info("===== ICICI UPI payment failed =====")
                        status = "Failed"
                        if "except_error" in response:
                            resp = response.get("except_error", "N/A")
                    ledgerModelService.update_upi_icici_status(id, "Success", self.client_ip_address,
                                                               "Merchant :: " + str(
                                                                   self.merchant_id), resp, message, UpiTranlogId,
                                                               UserProfile, SeqNo, MobileAppData, PayerRespCode,
                                                               BankRRN)

                elif mode_rec.lower() == "neft" or mode_rec.lower() == "rtgs":
                    urn = response.get("URN", "N/A")
                    status = response.get("STATUS", "N/A")
                    unique_id = response.get("UNIQUEID", "N/A")
                    resp = response.get("RESPONSE", "N/A")
                    req_id = response.get("REQID", payoutrequestmodel.beneficiaryAccount)
                    utr = response.get("UTRNUMBER", "N/A")
                    response_code = response.get("RESPONSECODE", "N/A")
                    message = response.get("MESSAGE", "N/A")
                    error_code = response.get("ERRORCODE", "N/A")
                    if status.lower() == "success" and resp.lower() == "success":
                        logger.info("===== ICICI neft/rtgs payment success =====")
                        status = "Success"
                    else:
                        logger.info("========= ICICI neft/rtgs payment failed =======")
                        status = "Failed"
                        if "except_error" in response:
                            resp = response.get("except_error", "N/A")
                    ledgerModelService.update_upi_icici_status(id=id, status="Success",
                                                               client_ip_address=self.client_ip_address,
                                                               created_by="Merchant :: " + str(
                                                                   self.merchant_id), remarks=resp,
                                                               system_remarks=message, bene_account_number=req_id,
                                                               UserProfile=response_code, SeqNo=error_code,
                                                               MobileAppData=resp, PayerRespCode=utr,
                                                               bank_ref_no=unique_id)

                elif mode_rec.lower() == "imps":
                    resp = response.get("success", "true")
                    message = response.get("Response", "Transaction Successful")
                    act_code = response.get("ActCode", "0")
                    trans_ref_no = response.get("TransRefNo", iciciPaymentRequestModel.get("data").get("tranRefNo"))
                    bank_rrn = response.get("BankRRN", icici_utils.generate_random_number())
                    bene_name = response.get("BeneName", "N/A")
                    act_code_desc = response.get("ActCodeDesc", "N/A")
                    if act_code == "0" and message == "Transaction Successful":
                        logger.info("===== ICICI imps payment success =====")
                        status = "Success"
                    else:
                        logger.info("===== ICICI imps payment failed =====")
                        status = "Failed"
                        if "except_error" in response:
                            resp = response.get("except_error", "N/A")
                    ledgerModelService.update_upi_icici_status(id=id, status="Success",
                                                               client_ip_address=self.client_ip_address,
                                                               created_by="Merchant :: " + str(
                                                                   self.merchant_id), remarks=resp,
                                                               system_remarks=message, bene_account_number=trans_ref_no,
                                                               UserProfile=bene_name, SeqNo="N/A",
                                                               MobileAppData=act_code_desc, PayerRespCode=act_code,
                                                               bank_ref_no=bank_rrn)

                ledgerModelService.update_trans_time(id, datetime.now(
                ), self.client_ip_address, "Merchant :: " + str(self.merchant_id))
                # =====================================================================

                # ---------------- status thread start --------------------------------
                merchant_id = self.merchant_id
                client_ip_address = self.client_ip_address

                class StatusThread(threading.Thread):
                    def run(self):
                        logger.info("===== ICICI status thread start =====")
                        log = Log_Model_Service(json=str({"merchant_id": merchant_id}), log_type="Thread",
                                                full_request={"orderId": ledgerModelService.payout_trans_id},
                                                client_ip_address=client_ip_address,
                                                server_ip_address=const.server_ip,
                                                remarks="Running service thread on icici status api for merchant id :: " + merchant_id)
                        logid = log.save()
                        logger.info("===== ICICI status thread waiting for 40 sec.... =====")
                        time.sleep(40)
                        logger.info("===== ICICI status thread continued =====")
                        if mode_rec.lower() == "upi":
                            logger.info("===== Processing ICICI status for UPI =====")
                            request_data = iciciStatusService.createUpiStatusRequesData(
                                vars(iciciPaymentRequestModel.get("data")))
                            status_response = iciciStatusService.processICICIStatus(request_data, header)
                            log.update_response(logid, str(status_response))
                            logger.info("status response : ", status_response)
                            resp = status_response.get("response", "N/A")
                            message = status_response.get("message", "N/A")
                            UpiTranlogId = status_response.get("UpiTranlogId", "N/A")
                            UserProfile = status_response.get("userProfile", "N/A")
                            SeqNo = status_response.get("SeqNo", "N/A")
                            MobileAppData = status_response.get("MoblieAppData", "N/A")
                            PayerRespCode = status_response.get("PayerRespCode", "N/A")
                            BankRRN = status_response.get("BankRRN", "null")
                            if resp == "0" and message == "Transaction Successful":
                                logger.info("===== ICICI status success =====")
                                status = "Success"
                            else:
                                logger.info("===== ICICI status failed =====")
                                status = "Failed"
                            ledgerModelService.update_upi_icici_status(id=id, status=status,
                                                                       client_ip_address=client_ip_address,
                                                                       created_by="Merchant :: " + str(
                                                                           merchant_id), remarks=resp,
                                                                       system_remarks=message,
                                                                       bene_account_number=UpiTranlogId,
                                                                       UserProfile=UserProfile, SeqNo=SeqNo,
                                                                       MobileAppData=MobileAppData,
                                                                       PayerRespCode=PayerRespCode,
                                                                       bank_ref_no=BankRRN)
                        elif mode_rec.lower() == "imps":
                            logger.info("===== Processing ICICI status for IMPS =====")
                            request_data = iciciStatusService.createImpsStatusRequesData(
                                iciciPaymentRequestModel.get("data"))
                            status_response = iciciStatusService.processICICIStatus(request_data, header)
                            imps_response = status_response.get("ImpsResponse", "N/A")
                            log.update_response(logid, str(status_response))
                            logger.info("status response : ", status_response)
                            ActCode = imps_response.get("ActCode", "N/A")
                            Response = imps_response.get("Response", "N/A")
                            BankRRN = imps_response.get("BankRRN", "N/A")
                            BeneName = imps_response.get("BeneName", "N/A")
                            TranRefNo = imps_response.get("TranRefNo", "N/A")
                            PaymentRef = imps_response.get("PaymentRef", "N/A")
                            TranDateTime = imps_response.get("TranDateTime", "N/A")
                            Amount = imps_response.get("Amount", "N/A")
                            BeneMMID = imps_response.get("BeneMMID", "N/A")
                            BeneMobile = imps_response.get("BeneMobile", "N/A")
                            BeneAccNo = imps_response.get("BeneAccNo", "N/A")
                            BeneIFSC = imps_response.get("BeneIFSC", "N/A")
                            RemMobile = imps_response.get("RemMobile", "N/A")
                            RemName = imps_response.get("RemName", "N/A")
                            RetailerCode = imps_response.get("RetailerCode", "N/A")
                            if ActCode == "0" and Response == "Transaction Successful":
                                logger.info("===== ICICI imps status success =====")
                                status = "Success"
                            else:
                                logger.info("===== ICICI imps status failed =====")
                                status = "Failed"
                            ledgerModelService.update_imps_icici_status(id=id, status=status,
                                                                        client_ip_address=client_ip_address,
                                                                        created_by="Merchant :: " + str(
                                                                            merchant_id), remarks=Response,
                                                                        system_remarks=RemMobile,
                                                                        bene_account_number=BeneAccNo,
                                                                        UserProfile=bene_name, SeqNo=PaymentRef,
                                                                        MobileAppData=BeneMMID,
                                                                        PayerRespCode=TranRefNo,
                                                                        TranDateTime=TranDateTime,
                                                                        RemName=RemName,
                                                                        RetailerCode=RetailerCode,
                                                                        bank_ref_no=BankRRN)

                        elif mode_rec.lower() == "rtgs" or mode_rec.lower() == "neft":
                            logger.info("===== Processing ICICI status for NEFT/RTGS =====")
                            request_data = iciciStatusService.createNeftAndRtgsStatusRequestData(
                                iciciPaymentRequestModel.get("data"))
                            status_response = iciciStatusService.processICICIStatus(request_data, header)
                            log.update_response(logid, str(status_response))
                            logger.info("status response : ", status_response)
                            STATUS = status_response.get("STATUS", "N/A")
                            URN = status_response.get("URN", "N/A")
                            UNIQUEID = status_response.get("UNIQUEID", "N/A")
                            UTRNUMBER = status_response.get("UTRNUMBER", "N/A")
                            RESPONSE = status_response.get("RESPONSE", "N/A")
                            if STATUS.lower() == "success":
                                logger.info("===== ICICI status success =====")
                                status = "Success"
                            elif STATUS.lower() == "pending":
                                logger.info("======== ICICI status pending =====")
                                status = "Pending"
                            else:
                                logger.info("======= ICICI status failed")
                                status = "Failed"
                            ledgerModelService.update_neft_rtgs_icici_status(id=id, status=status,
                                                                             client_ip_address=client_ip_address,
                                                                             created_by="Merchant :: " + str(
                                                                                 merchant_id), utr=UTRNUMBER, urn=URN,
                                                                             uniqueId=UNIQUEID, response=RESPONSE
                                                                             )

                # StatusThread().start()

                # ---------------- status thread end ----------------------------------

                class WebhookThread(threading.Thread):
                    def run(self):
                        log = Log_Model_Service(json=str({"merchant_id": merchant_id}), log_type="Thread",
                                                client_ip_address=client_ip_address,
                                                server_ip_address=const.server_ip,
                                                remarks="Running service thread on webhook apis for merchant id :: " + merchant_id)
                        log.save()
                        transhistory = Ledger_model_services.Ledger_Model_Service.fetch_by_id(
                            id=ledger_id, client_ip_address=client_ip_address, created_by="system")

                        webhookrequest = Webhook_Request_Model_Service()
                        webhookrequest.payout_trans_id = transhistory.payout_trans_id
                        webhookrequest.hit_init_time = datetime.now()
                        webhookrequest.status = False
                        id = webhookrequest.save()

                        webhooks = Webhook_Model_Service.fetch_by_merchant_id_payout(
                            merchant_id, client_ip_address)
                        print("Webhook Started at :: " + str(webhooks.webhook))
                        if webhooks is not None and not webhooks.is_instant:
                            print("Interval Webhook :: " +
                                  str(webhooks.time_interval) + " min ")
                            interval = webhooks.time_interval
                            time.sleep(60 * interval)
                        if webhooks is None:
                            pass
                        else:
                            transhistoryJson = Ledger_model_services.Ledger_Model_Service.fetch_by_id_tojson(
                                id=ledger_id, client_ip_address=client_ip_address, created_by="system")
                            response = requests.post(
                                webhooks.webhook, json=transhistoryJson)
                            print("First Response from webhook :: " + response.text)
                            if response.status_code != 200:
                                for i in range(webhooks.max_request):
                                    interval = webhooks.time_interval
                                    time.sleep(60 * interval)
                                    response = requests.post(
                                        webhooks.webhook, json=transhistoryJson)
                                    print(
                                        str(i) + "th response from webhook :: " + response.text)
                                    if response.status_code == 200:
                                        break
                            if response.status_code == 200:
                                Webhook_Request_Model_Service.update_webhook(
                                    id, True, response.text)
                            else:
                                print("updating response as false")
                                Webhook_Request_Model_Service.update_webhook(
                                    id, False, response.text)

                return ["Payout Done",
                        {"orderId": ledgerModelService.customer_ref_no, "amount": ledgerModelService.amount,
                         "status": "PROCESSING", "requestedDatetime": str(datetime.now()).split(".")[0]}, True]
            else:
                return [message, {}, False]
        except Exception as e:
            import traceback
            logger.error(traceback.format_exc(), exc_info=True)
            return [e.args, {}, False]
