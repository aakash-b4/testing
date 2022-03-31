# from django.shortcuts import render
# Create your views here.


import json
from django.db.models import query
from django.core import serializers

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
from apis.view_api import client
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

from ..models import MerchantModel,RoleModel, BOUserModel







# from .models import MerchantModel,RoleModel
from sabpaisa import auth

from datetime import datetime

from ..bank_services import ICICI_service

from ..other_service import login_service,signup_service

from sabpaisa import auth



class LoginRequestAdminAPI(APIView):
    @swagger_auto_schema(request_body=login_docs.request_admin,responses=login_docs.response_login_request)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(json=str({"username":req.data["username"]}),log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            print(req.data)
            login=login_service.Login_service(username=req.data["username"],password=req.data["password"],client_ip_address=req.META['REMOTE_ADDR'])
            res = login.login_request_admin()
            if(res==False):
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"User Not Found","response_code":"0"})
                return Response({"message":"User Not Found","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if req.data["username"]=="admin":
                    api_key=auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).encrypt(str(res["user_id"]))
                   
                    return Response({"auth_token":str(api_key)[2:].replace("'",""),"merchant_id":res["user_id"],"jwt_token":res["jwt_token"],"username":res["username"],"user_token":res['user_token'],"response_code":"1"},status=status.HTTP_200_OK)
                print("sonuggdsbbbccccccccccccccccccccccccccccc")
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP sent","verification_token":res,"response_code":"1"})
                return Response({"message":"OTP has been sent to Registered Email and Mobile Number","verification_token":res,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"message":"Some error occured","Error_Code":e.args,"response_code":"2"},status=status.HTTP_409_CONFLICT)

class LoginRequestAPI(APIView):
    @swagger_auto_schema(request_body=login_docs.request,responses=login_docs.response_login_request)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(json=str({"username":req.data["username"]}),log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            print(req.data)
            login=login_service.Login_service(username=req.data["username"],password=req.data["password"],client_ip_address=req.META['REMOTE_ADDR'])
            res = login.login_request()
            if(res==False):
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"User Not Found","response_code":"0"})
                return Response({"message":"User Not Found","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            else:
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP sent","verification_token":res,"response_code":"1"})
                if req.data["username"]=="DJ_merchant":
                    api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(str(res["user_id"]))
                    return Response({"auth_token":str(api_key)[2:].replace("'",""),"merchant_id":res["user_id"],"jwt_token":res["jwt_token"],"username":res["username"],"user_token":res['user_token'],"response_code":"1"},status=status.HTTP_200_OK)
                return Response({"message":"OTP has been sent to Registered Email and Mobile Number","verification_token":res,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"message":"Some error occured","Error_Code":e.args,"response_code":"2"},status=status.HTTP_409_CONFLICT)

class LoginVerificationAPI(APIView):
    @swagger_auto_schema(request_body=login_docs.verification,responses=login_docs.response_login_verification)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
            login=login_service.Login_service.login_verification(req.data['verification_code'],req.data["otp"],req.META['REMOTE_ADDR'],req.data['geo_location'],req.data["type"])
            if(login=="OTP Expired"):
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP Expired","response_code":"0"})
                return Response({"message":"OTP Expired","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            elif login==False:
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"OTP is not valid","response_code":"0"})
                return Response({"message":"OTP is not valid","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            else:
                # print(str(login[0]))
                
                if req.data['type']=="back_office":
                    api_key=auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).encrypt(str(login["user_id"]))
                else:
                    api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(str(login["user_id"]))

                Merchant= login['username']
                data1= BOUserModel.objects.get(username= Merchant)
                
                auth_key=data1.auth_key
                auth_iv= data1.auth_iv
               
                Log_model_services.Log_Model_Service.update_response(logid,{"auth_token":str(api_key)[2:].replace("'",""),"response_code":"1"})
                return Response({"auth_key":str(auth_key),"auth_iv":str(auth_iv),"auth_token":str(api_key)[2:].replace("'",""),"merchant_id":login["user_id"],"jwt_token":login["jwt_token"],"username":login["username"],"user_token":login['user_token'],"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"Error_Code":e.args,"response_code":"2"})
            return Response({"Error_Code":e.args,"response_code":"2"},status=status.HTTP_400_BAD_REQUEST)
class ResendLoginOTP(APIView):
    @swagger_auto_schema(request_body=login_docs.resend_otp_request,responses=login_docs.response_login_request)
    def post(self,req):
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="post request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        try:
         login=login_service.Login_service.resend_otp(req.data["verification_code"],req.META['REMOTE_ADDR'],req.data["type"])
        #  api_key=auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(login)
         Log_model_services.Log_Model_Service.update_response(logid,{"verification_token":login,"response_code":"1"})
         return Response({"message":"OTP sent ","verification_token":login,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"Error":e.args,"response_code":'2'})
            return Response({"Error":e.args,"response_code":'2'},status=status.HTTP_400_BAD_REQUEST)
        
