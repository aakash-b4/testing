# from django.shortcuts import render
# Create your views here.


from logging import log
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

from ..bank_services import ICICI_service

from ..other_service import login_service,signup_service

from sabpaisa import auth

class GetLogs(APIView):
    @swagger_auto_schema(responses=log_docs.response_dict,request_body=log_docs.request)
    def post(self,req,page,length):
        req.session["kan"]="cs"
        authKey = const.admin_AuthKey
        authIV = const.admin_AuthIV
        resp = req.headers["auth_token"]
        start_date=req.data['start']
        end_date=req.data['end']
        if start_date!="all" or end_date!="all":
            start_date=datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_date=datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        
        merchant = auth.AESCipher(authKey,authIV).decrypt(resp)
        clientModel=BO_user_services.BO_User_Service.fetch_by_id(id=merchant)
        print(clientModel,"clientModel")
        if clientModel == None:
            return  Response({"message":"client not found"},status=status.HTTP_401_UNAUTHORIZED)
        # clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
        #     id=merchant, created_by=str(merchant), client_ip_address=req.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        print(clientModel.auth_iv,"auth iv")
        request_obj = "path:: "+req.path+" :: headers::"+str(req.headers)+" :: meta_data:: "+str(req.META)+"data::"+str(req.data)
        logs = Log_model_services.Log_Model_Service(log_type="get request on "+req.path,client_ip_address=req.META['REMOTE_ADDR'],server_ip_address=const.server_ip,full_request=request_obj,remarks="get request on "+req.path+" for fetching the log records")
        logid=logs.save()
        # merchant=MerchantModel.objects.get(id=merchant)
        role = RoleModel.objects.get(id=clientModel.role_id)
        try:
            if page=="all" and length != "all":
                return JsonResponse({"Message":"page and length format does not match"},status=status.HTTP_406_NOT_ACCEPTABLE)
            logs = Log_model_services.Log_Model_Service.fetch_all_logs_in_parts(page,length,start_date,end_date)
            #auth.AESCipher(authKey, authIV).encrypt(logsser.data)
            # print(logs)
            if len(logs)==0:
               
                return Response({"data_length": len(logs[1]), "data": None})
            if page == "all":
                logsser=LogsSerializer(logs[0],many=True)
                enc_data=logsser.data
               
                if clientModel.is_encrypt :
                  enc_data = auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))
                
                print(enc_data)
                print(authKey,authIV,"AUTH KEY , AUTH IV")
                return Response({"data_length": len(logs[1]), "data": str(enc_data)})
            # page=int(page)
            # if page>logs[1]:
            #  page=logs[1]-1
            logsser=LogsSerializer(logs[0],many=True)
            # # print(logs[0][page],len(logs[0][page]))
            # # logsser=LogsSerializer(logs[0][page],many=True)
            enc_data=logsser.data
            # print(authKey,authIV,"AUTH KEY , AUTH IV")
            # if clientModel.is_encrypt :
            #       enc_data = auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))
            # Log_model_services.Log_Model_Service.update_response(logid, str({"data_length": len(
            #     logs[0][page]), "data": enc_data}))
            
            # # print(merchant.id)
            # enc_data=logsser.data
            # print(enc_data)
            # print(role.role_name)
            if clientModel.is_encrypt :
             print("if")
             enc_data = auth.AESCipher(authKey, authIV).encrypt(str(logsser.data))
            
            print(enc_data)
            print(authKey,authIV,"AUTH KEY , AUTH IV")
            return Response({"data_length": logs[1], "data": enc_data})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid, str({"Message":"some error","Error":e.args}))
            return Response({"Message":"some error","Error":e.args})
        