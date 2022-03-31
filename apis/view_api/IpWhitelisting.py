import re
from django.db.models import query


from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import permissions
# from apis.database_models.Test import TestModel

from rest_framework.exceptions import server_error
# from apis.bank_services.IFDC_service import payment
from django.http import *
from rest_framework import generics
from django.shortcuts import *
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apis.database_service import Beneficiary_model_services
from ..API_docs import payout_docs,auth_docs,login_docs,payoutTransactionEnquiry_docs,addBalance_docs,addBeneficiary_docs,log_docs
from datetime import datetime
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


from sabpaisa import auth
from ..database_service.IpWhitelisting_model_service import IpWhiteListing_Model_Service

class CreateIpWhiteList(APIView):
    def post(self, request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="add ip whitelisting request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            auth_token = request.headers.get("auth_token")
            merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
            if(clientModel==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "0"})
                return Response({"message":"merchant id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            query = request.data.get("query")
            if(clientModel.is_encrypt==True):
                decrypted_query = auth.AESCipher(clientModel.auth_key,clientModel.auth_iv).decrypt(query)
                query = ast.literal_eval(str(decrypted_query))
            ip  = query.get("ip_address")
            service = IpWhiteListing_Model_Service(ip_add=ip,merchant_id=merchantId)
            resp = service.save()
            if(resp ==0):
                return Response({"message":"duplicate entry found","response_code": "0"},status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({"message":"data saved","response_code":"1"},status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

class DeleteIp(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="delete ip whitelisting request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            auth_token = request.headers.get("auth_token")
            merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
            if(clientModel==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "0"})
                return Response({"message":"merchant id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            query = request.data.get("query")
            if(clientModel.is_encrypt==True):
                decrypted_query = auth.AESCipher(clientModel.auth_key,clientModel.auth_iv).decrypt(query)
                query = ast.literal_eval(str(decrypted_query))
            ip  = query.get("ip_address")
            service = IpWhiteListing_Model_Service(ip_add=ip,merchant_id=merchantId)
            resp = service.deleteIp()
            if(resp == 0):
                return Response({"message":"deleted unsuccessfully IP not found","response_code":"0"},status=status.HTTP_404_NOT_FOUND)
            return Response({"message":"deleted successfully","response_code":"1"},status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

    
class fetchIpsByMerchantId(APIView):
    def get(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="delete ip whitelisting request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            auth_token = request.headers.get("auth_token")
            merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchantId, created_by="merchantid :: "+merchantId, client_ip_address=request.META['REMOTE_ADDR'])
            if(clientModel==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "0"})
                return Response({"message":"merchant id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            service = IpWhiteListing_Model_Service()
            resp = service.fetchIpsByMerchant(merchantId)
            if(resp==0):
                return Response({"message":"data found","data":None,"response_code": "0"},status=status.HTTP_404_NOT_FOUND)
            if(clientModel.is_encrypt==True):
                encResp = auth.AESCipher(clientModel.auth_key,clientModel.auth_iv).encrypt(str(resp))
                return Response({"message":"data found","data":encResp,"response_code": "1"},status=status.HTTP_200_OK)
            return Response({"message":"data found","data":resp,"response_code": "1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})