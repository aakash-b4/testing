import ast
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import *
from rest_framework.views import APIView

from apis.database_service.Ledger_model_services import *
from apis.other_service.enquiry_service import *
from sabpaisa import auth
from .. import const
from ..API_docs import payout_docs, payoutTransactionEnquiry_docs, addBalance_docs
from ..database_models.ModeModel import ModeModel
from ..database_models.VariableModel import VariableModel
from ..database_service import BO_user_services
from ..database_service import Client_model_service, Bank_model_services
from ..database_service import Merchant_mode_services
from ..database_service import Mode_model_services
from ..database_service.DailyLedger_model_services import DailyLedger_Model_Service
from ..models import RoleModel
from ..other_service import payout_service

info_logger = logging.getLogger("info_logger")
debug_logger = logging.getLogger("debug_logger")
error_logger = logging.getLogger("error_logger")


class bankApiPaymentView(APIView):
    # permission_classes = (IsAuthenticated, )
    @swagger_auto_schema(request_body=payout_docs.request, responses=payout_docs.response_schema_dict)
    def post(self, req):
        try:

            request_obj = "path::" + req.path + "headers::" + str(req.headers) + "meta_data::" + str(
                req.META) + "data::" + str(req.data)
            # payment_service=IFDC_service.payment.Payment()
            api_key = req.headers['auth_token']
            merchant_id = auth.AESCipher(const.AuthKey, const.AuthIV).decrypt(api_key)

            encrypted_code = req.data["query"]
            mode = req.data['mode']
            variable = VariableModel.objects.filter(variable_name="getBalance")
            if variable[0].variable_value != "first":
                daily = DailyLedger_Model_Service.fetch_by_date_and_merchant_id(merchant_id, date.today())
                if daily == None:
                    return Response(
                        {"message": "Some calculation is proccessing please wait and retry again with same request",
                         "responseCode": "0"}, status=status.HTTP_400_BAD_REQUEST)

            log = Log_model_services.Log_Model_Service(json=str({"merchant_id": merchant_id}),
                                                       log_type="Post request at " + req.path + " slug",
                                                       client_ip_address=req.META['REMOTE_ADDR'],
                                                       server_ip_address=const.server_ip, full_request=request_obj)
            logid = log.save()
            client = Client_model_service.Client_Model_Service.fetch_by_id(merchant_id, req.META['REMOTE_ADDR'],
                                                                           "merchant id :: " + merchant_id)
            if not client.is_transactable:
                return Response({"message": "Your are not permitted to perform transactions please contact sabpaisa",
                                 "responseCode": 0}, status=status.HTTP_401_UNAUTHORIZED)
            mode_rec = Mode_model_services.Mode_Model_Service.fetch_by_mode(mode)
            if mode_rec == None:
                return Response({"message": "mode not valid", "responseCode": "0"}, status=status.HTTP_400_BAD_REQUEST)
            merchant_mode = Merchant_mode_services.Merchant_Mode_Service.fetch_by_merchant_id_and_mode(
                mode_id=mode_rec.id, merchant_id=merchant_id)
            if len(merchant_mode) == 0:
                return Response({"message": "merchant mode not valid", "responseCode": "0"},
                                status=status.HTTP_400_BAD_REQUEST)
            bank = Bank_model_services.Bank_model_services.fetch_by_id(merchant_mode[0].bank_partner_id,
                                                                       req.META['REMOTE_ADDR'],
                                                                       "merchant id :: " + merchant_id)
            # print("bank::"+str(bank))
            payout = payout_service.PayoutService(merchant_id=merchant_id, encrypted_code=encrypted_code,
                                                  client_ip_address=req.META['REMOTE_ADDR'])
            if bank.bank_name.lower() == "icici":
                info_logger.info("Executing ICICI payment request")
                res = payout.excuteICICI(mode_rec=mode)
            elif bank.bank_name == "PAYTM":
                res = payout.excutePAYTM(mode_rec=mode)
            else:
                res = payout.excuteIDFC()
            info_logger.info("response >>> " + str(res))
            if res[0] == "Payout Done":
                # merchant=MerchantModel.objects.get(id=merchant_id)
                # role = RoleModel.objects.get(id=merchant.role)
                enc_str = res[1]
                if client.is_encrypt:
                    enc_str = str(auth.AESCipher(client.auth_key, client.auth_iv).encrypt(str(res[1])))[2:].replace("'",
                                                                                                                    "")

                Log_model_services.Log_Model_Service.update_response(logid, {"message": res, "responseCode": "1"})
                return Response({"message": "Payout Done", 'resData': enc_str, "responseCode": "1"},
                                status=status.HTTP_200_OK)
            elif not res[2]:
                Log_model_services.Log_Model_Service.update_response(logid, {"message": res, "responseCode": "0"})
                return Response({"message": res[0], "responseCode": "0"}, status=status.HTTP_400_BAD_REQUEST)
            elif res[0] == False:
                Log_model_services.Log_Model_Service.update_response(logid, {"message": "credential not matched",
                                                                             "responseCode": "3"})
                return Response({"message": "credential not matched", "responseCode": "3"},
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                Log_model_services.Log_Model_Service.update_response(logid, {"message": res, "responseCode": "2"})
                return Response({"message": res, "responseCode": "2"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            import traceback
            error_logger.error("error in payout request::" + traceback.format_exc())
            #  Log_model_services.Log_Model_Service.update_response(logid,{"message":e.args,"responseCode":"2"})
            return Response({"message": "Some Technical error", "responseCode": "2"}, status=status.HTTP_204_NO_CONTENT)


class paymentEnc(APIView):
    @swagger_auto_schema(request_body=payoutTransactionEnquiry_docs.request,
                         responses=payoutTransactionEnquiry_docs.response_schema_dict)
    def post(self, req):

        try:
            data = req.data["query"]
            auth_token = req.headers["auth_token"]
            print("auth token :: " + auth_token)
            merchant_id = auth.AESCipher(const.AuthKey, const.AuthIV).decrypt(auth_token)
            print("merchant id :: " + merchant_id)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(id=merchant_id,
                                                                                created_by="Merchant :: " + str(
                                                                                    merchant_id),
                                                                                client_ip_address=req.META[
                                                                                    'REMOTE_ADDR'])
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            encResp = data
            if clientModel.is_encrypt:
                encResp = auth.AESCipher(authKey, authIV).decrypt(data)
            customer_ref = encResp.split(":")[1].replace('"', '').replace(' ', '')
            print("customer ref :: " + customer_ref)
            recs = enquiry_service.get_enc(merchant_id, customer_ref, req.META['REMOTE_ADDR'],
                                           created_by="Merchant id :: " + str(merchant_id))
            response = []

            if recs is not None:
                for rec in recs:
                    payments_mode = ModeModel.objects.get(id=rec.payment_mode_id)

                    res = {

                        'payoutTransactionId': rec.payout_trans_id,
                        'amount': rec.amount,
                        'transType': rec.trans_type,
                        'statusType': rec.type_status,
                        'bankRefNo': rec.bank_ref_no,
                        'orderId': rec.customer_ref_no,
                        'beneficiaryAccountName': rec.bene_account_name,
                        'beneficiaryAccountNumber': rec.bene_account_number,
                        'beneficiaryIFSC': rec.bene_ifsc,
                        "upiId": rec.upi_id,
                        'transStatus': rec.trans_status,
                        'mode': payments_mode.mode
                    }
                    response.append(res)

                enc = response
                # print("roleName :: "+role.role_name)
                if clientModel.is_encrypt:
                    enc = str(auth.AESCipher(authKey, authIV).encrypt(str(res)))[2:].replace("'", "")
                # elif not const.test_merchants:
                #     enc = str(auth.AESCipher(authKey,authIV).encrypt(str(res)))[2:].replace("'","")
                return Response({"message": "data found", "resData": enc, "responseCode": "1"})
            else:
                return Response({"message": "NOT_FOUND", "responseCode": "0"})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"message": e.args})


class addBalanceApi(APIView):
    @swagger_auto_schema(request_body=addBalance_docs.request, responses=addBalance_docs.response_schema_dict)
    def post(self, request):
        request_obj = "path:: " + request.path + " :: headers::" + \
                      str(request.headers) + " :: meta_data:: " + \
                      str(request.META) + "data::" + str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="Post request at " + request.path + " slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'],
                                                   server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        authKey = const.AuthKey
        authIV = const.AuthIV
        merchant = request.headers["auth_token"]
        if (merchant == ""):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"message": "merchant code missing", "responseCode": "0"})
            return Response({"message": "merchant code missing", "data": None, "responseCode": "3"},
                            status=status.HTTP_400_BAD_REQUEST)
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(merchant)
        created_by = "merchant ::" + decMerchant
        query = request.data.get("query")
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=decMerchant, created_by=created_by, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        # start
        role = RoleModel.objects.get(id=clientModel.role_id)
        if clientModel.is_encrypt == False:
            print("hello")
            decResp = request.data.get("query")
            print(decResp)
            res = ast.literal_eval(str(decResp))
            response = Ledger_Model_Service.addBal(res, client_ip_address=request.META['REMOTE_ADDR'],
                                                   merchant=decMerchant, clientCode=clientModel.client_code)
            return Response({"data": str(response), "responseCode": "1"})
        # end
        decResp = auth.AESCipher(authKey, authIV).decrypt(str(query))
        res = ast.literal_eval(decResp)
        response = Ledger_Model_Service.addBal(res, client_ip_address=request.META['REMOTE_ADDR'], merchant=decMerchant,
                                               clientCode=clientModel.client_code)
        print(authKey + " " + authIV)
        encResponse = str(auth.AESCipher(authKey, authIV).encrypt(response))[2:].replace("'", "")
        Log_model_services.Log_Model_Service.update_response(
            logid, {"message": str(encResponse), "responseCode": "1"})
        return Response({"message": "data saved succefully", "data": str(encResponse), "responseCode": "1"},
                        status=status.HTTP_200_OK)


# class adminAddBalance(APIView):
#     def post(self,request):
#         request_obj = "path:: "+request.path+" :: headers::" + \
#             str(request.headers)+" :: meta_data:: " + \
#             str(request.META)+"data::"+str(request.data)

#         log = Log_model_services.Log_Model_Service(log_type="addCharge request at "+request.path+" slug",
#                                                    client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
#         logid = log.save()
#         try:
#             query = request.headers.get("auth_token")
#             adminId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(query)
#             admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
#             if(admin==None):
#                 Log_model_services.Log_Model_Service.update_response(
#                 logid, {"message": "admin code missing", "responseCode": "0"})
#                 return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
#             authKey = admin.auth_key
#             authIV = admin.auth_iv
#             if(admin.is_encrypt != True):

#         except Exception as e:
#             import traceback
#             print(traceback.format_exc())
#             Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"responseCode":"2"})
#             return Response({"message":"some error","Error":e.args})


class addBalance(APIView):
    def post(self, request):
        request_obj = "path:: " + request.path + " :: headers::" + \
                      str(request.headers) + " :: meta_data:: " + \
                      str(request.META) + "data::" + str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="addBalance request at " + request.path + " slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'],
                                                   server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            header = request.headers.get("auth_token")
            adminId = auth.AESCipher(const.admin_AuthKey, const.admin_AuthIV).decrypt(header)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if (admin == None):
                Log_model_services.Log_Model_Service.update_response(
                    logid, {"message": "admin code missing", "responseCode": "0"})
                return Response({"message": "admin id does not exist", "Response code": "0"},
                                status=status.HTTP_404_NOT_FOUND)
            requestBody = request.data.get("query")
            if (admin.is_encrypt == True):
                decRequest = auth.AESCipher(admin.auth_key, admin.auth_iv).decrypt(requestBody)
                requestBody = ast.literal_eval(str(decRequest))
                response = Ledger_Model_Service.addAmount(requestBody, client_ip_address=request.META['REMOTE_ADDR'],
                                                          admin=adminId, amount=requestBody.get("amount"))
                return Response({"message": "balance added", "responseCode": "1"}, status=status.HTTP_201_CREATED)

            response = Ledger_Model_Service.addAmount(requestBody, client_ip_address=request.META['REMOTE_ADDR'],
                                                      admin=adminId, amount=requestBody.get("amount"))

            return Response({"message": "balance added", "responseCode": "1"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,
                                                                 {"message": "Some error occured", "Error_Code": e.args,
                                                                  "responseCode": "2"})
            return Response({"message": "some error", "Error": e.args})
