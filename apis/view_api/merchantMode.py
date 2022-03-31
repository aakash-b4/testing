from rest_framework.views import APIView
from apis.database_service import merchant_mode_service
from apis.view_api.beneficiary import merchantFetchBeneficiary
from ..serializersFolder.serializers import LogsSerializer
#from .serializers import *
# from .models import *
import ast
from ..other_service import payout_service
from ..database_models import LedgerModel,ModeModel
from apis.database_service.Ledger_model_services import *
from django.http.response import JsonResponse
from apis.other_service.enquiry_service import *
from apis.database_service.Beneficiary_model_services import *
from ..database_service import Client_model_service,Bank_model_services
from rest_framework.parsers import JSONParser
from ..database_service import Client_model_service,Bank_model_services,IpWhitelisting_model_service
from django.contrib.auth.models import User
# from .database_service import Client_model_service,Ledger_model_services
from rest_framework.permissions import IsAuthenticated
from .. import const
from ..Utils import randomstring
from ..database_service import BO_user_services

from ..models import MerchantModel,RoleModel

# from .models import MerchantModel,RoleModel
from sabpaisa import auth

from datetime import datetime

from ..bank_services import ICICI_service

from ..other_service import login_service,signup_service

from rest_framework.response import *
from sabpaisa import auth
from ..database_service.IpWhitelisting_model_service import IpWhiteListing_Model_Service

class addMerchantMode(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="add merchant mode request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            header = request.headers.get("auth_token")
            adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if(admin==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
                return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            query = request.data.get("query")
            if(admin.is_encrypt==True):
                decrypted_query = auth.AESCipher(admin.auth_key,admin.auth_iv).decrypt(query)
                query = ast.literal_eval(str(decrypted_query))
            merchant_id = query.get("merchant_id")
            bank_partner_id = query.get("bank_partner_id")
            mode_id = query.get("mode_id")
            service = merchant_mode_service.Merchant_mode_service(merchant_id=merchant_id,bank_partner_id=bank_partner_id,mode_id=mode_id)
            resp = service.save(admin_id=adminId)
            if(resp == 0):
                return Response({"message":"duplicate data found","response_code":"0"},status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({"message":"data saved","response_code":"1"},status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

class fetchMerchantModes(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="fetch Merchant Mode request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            header = request.headers.get("auth_token")
            adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if(admin==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
                return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            service = merchant_mode_service.Merchant_mode_service()
            
            query = request.data.get("query")
            if(admin.is_encrypt==True):
                decrypted_query = auth.AESCipher(admin.auth_key,admin.auth_iv).decrypt(query)
                query = ast.literal_eval(str(decrypted_query))
            merchant_id = query.get("merchant_id")
            
            if(merchant_id == "all"):
                resp =  service.fetchAllMerchantModes()
            else:
                resp = service.fetchMerchantModeById(merchant_id=merchant_id)
            
            if(resp == 0):
                return Response({"message":"data not found","data":None,"response_code":"0"},status=status.HTTP_404_NOT_FOUND)
            if(admin.is_encrypt==True):
                resp = auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(resp))
            return Response({"message":"data found","data":resp,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

# class deleteMerchantMode(APIView):
#     def post(self,request):
#         request_obj = "path:: "+request.path+" :: headers::" + \
#             str(request.headers)+" :: meta_data:: " + \
#             str(request.META)+"data::"+str(request.data)

#         log = Log_model_services.Log_Model_Service(log_type="delete Merchant Mode by merchant id request at "+request.path+" slug",
#                                                    client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
#         logid = log.save()
#         try:
#             header = request.headers.get("auth_token")
#             adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
#             admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
#             if(admin==None):
#                 Log_model_services.Log_Model_Service.update_response(
#                 logid, {"Message": "admin code missing", "response_code": "0"})
#                 return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
#             service = merchant_mode_service.Merchant_mode_service()
#             query = request.data.get("query")
#             if(admin.is_encrypt==True):
#                 decrypted_query = auth.AESCipher(admin.auth_key,admin.auth_iv).decrypt(query)
#                 query = ast.literal_eval(str(decrypted_query))
#                 print("query = ",str(query))
#             merchant_id = query.get("merchant_id")
#             mode_id = query.get("mode_id")
#             bank_partner_id=query.get("bank_partner_id")
#             service = merchant_mode_service.Merchant_mode_service()
#             resp = service.deleteMerchantMode(merchant_id=merchant_id,admin_id=adminId,mode_id=mode_id,bank_partner_id=bank_partner_id)
#             if(resp == 0):
#                 return Response({"message":"data not found","response_code":"0"},status=status.HTTP_404_NOT_FOUND)
#             return Response({"message":"deleted successfully","reponse_code":"1"},status=status.HTTP_200_OK)
#         except Exception as e:
#             import traceback
#             print(traceback.format_exc())
#             Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
#             return Response({"Message":"some error","Error":e.args})



class deleteMerchantMode(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="delete Merchant Mode by merchant id request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            header = request.headers.get("auth_token")
            adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if(admin==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
                return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            service = merchant_mode_service.Merchant_mode_service()
            query = request.data.get("query")
            if(admin.is_encrypt==True):
                decrypted_query = auth.AESCipher(admin.auth_key,admin.auth_iv).decrypt(query)
                query = ast.literal_eval(str(decrypted_query))
                print("query = ",str(query))
            merchant_id = query.get("merchant_id")
            mode_id = query.get("mode_id")
            bank_partner_id=query.get("bank_partner_id")
            stat=query.get("status")
            service = merchant_mode_service.Merchant_mode_service()
            resp = service.deleteMerchantMode(merchant_id=merchant_id,admin_id=adminId,mode_id=mode_id,bank_partner_id=bank_partner_id,status=stat)
            if(resp == 0 or resp == -1):
                return Response({"message":"data not found","response_code":"0"},status=status.HTTP_404_NOT_FOUND)
            return Response({"message":"updated successfully","reponse_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})