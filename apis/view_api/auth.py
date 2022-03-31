# from django.shortcuts import render
# Create your views here.


from django.db.models import query


from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
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

# from ..bank_services import ICICI_service
from ..bank_services import ICICI_service

from ..other_service import login_service,signup_service
from ..database_models.BOUserModel import BOUserModel

from sabpaisa import auth


class AuthAdmin(APIView):
    @swagger_auto_schema(request_body=auth_docs.request_admin,responses=auth_docs.admin_response_dict)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        user = req.data
        print("req data::"+str(req.data))
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        print("log::"+str(logid))
        try:
            val=signup_service.Signup_Service(user=user,client_ip_address=req.META['REMOTE_ADDR']).AdminSignup()
            api_key=auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).encrypt(str(val['merchant_id']))
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"user created","user_id":val['merchant_id'],"response_code":"1","CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()})
            return Response({"Message":"user created","response_code":"1","user_id":val['merchant_id'],"AUTH_TOKEN":str(api_key)[2:].replace("'",""),"CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())

            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"some error","error":e.args,"trace_back":e.with_traceback(e.__traceback__)})
            
            return Response({"Message":"some error","error":e.args},status=status.HTTP_400_BAD_REQUEST)

class Auth(APIView):
    @swagger_auto_schema(request_body=auth_docs.request,responses=auth_docs.response_schema_dict)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        user = req.data
        print("req data::"+str(req.data))
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        print("log::"+str(logid))
        try:
            
            val=signup_service.Signup_Service(user=user,client_ip_address=req.META['REMOTE_ADDR']).SignUp()
            api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(str(val['merchant_id']))
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"user created","merchant_id":val['merchant_id'],"AUTH_TOKEN":str(api_key)[2:].replace("'",""),"response_code":"1","CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()})
            return Response({"Message":"user created","response_code":"1","merchant_id":val['merchant_id'],"AUTH_TOKEN":str(api_key)[2:].replace("'",""),"CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"some error","error":e.args,"trace_back":e.with_traceback(e.__traceback__)})
            
            return Response({"Message":"some error","error":e.args},status=status.HTTP_400_BAD_REQUEST)

class Merchant_Auth(APIView):
    @swagger_auto_schema(request_body=auth_docs.request,responses=auth_docs.response_schema_dict)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        user = req.data

        print("req data::"+str(req.data))
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+req.path+" slug",client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj)
        logid=log.save()
        print("log::"+str(logid))
        try:
            admin_id = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(req.headers["auth_token"])
            if len(BOUserModel.objects.filter(id=int(admin_id)))<0:
                raise Exception("admin is not valid")
            val=signup_service.Signup_Service(user=user,client_ip_address=req.META['REMOTE_ADDR']).SignUp()
            api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(str(val['merchant_id']))
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"user created","merchant_id":val['merchant_id'],"AUTH_TOKEN":str(api_key)[2:].replace("'",""),"response_code":"1","CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()})
            return Response({"Message":"user created","response_code":"1","merchant_id":val['merchant_id'],"AUTH_TOKEN":str(api_key)[2:].replace("'",""),"CLIENT_AUTH_KEY":val['client'].auth_key,"CLIENT_AUTH_IV":val['client'].auth_iv,"token":val['token'].json()},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            
            Log_model_services.Log_Model_Service.update_response(logid,{"Message":"some error","error":e.args,"trace_back":e.with_traceback(e.__traceback__)})
            
            return Response({"Message":"some error","error":e.args},status=status.HTTP_400_BAD_REQUEST)