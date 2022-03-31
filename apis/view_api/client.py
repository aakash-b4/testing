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

from apis.database_service import *
from ..API_docs import payout_docs,auth_docs,login_docs,payoutTransactionEnquiry_docs,addBalance_docs,addBeneficiary_docs,log_docs,ledgers_docs
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

class allMerchants(APIView):
    def get(self,request,page,length):
        authToken = request.headers.get("auth-token")
        adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(authToken)
        try:
            if page=="all" and length != "all":
                return JsonResponse({"Message":"page and length format does not match"},status=status.HTTP_406_NOT_ACCEPTABLE)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if(admin==None):
                return Response({"message":"admin id does not exist"},status=status.HTTP_401_UNAUTHORIZED)
            request_obj = "path:: "+request.path+" :: headers::" + \
                str(request.headers)+" :: meta_data:: " + \
                str(request.META)+"data::"+str(request.data)
            log = Log_model_services.Log_Model_Service(log_type="fetchBeneficiary request at "+request.path+" slug",
                                                    client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
            logid = log.save()
            resp = Client_model_service.Client_Model_Service.get_all_merchants(page,length)
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": str(resp), "response_code": "1"})
            if(admin.is_encrypt==True):
                encResp = str(auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(resp)))[2:].replace("'","")
                return Response({"message":"data found", "Response code":"1","data":str(encResp)})
            return Response({"message":"Data found", "Response code":"1","data":resp})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid, str({"Message":"some error","Error":e.args}))
            return Response({"Message":"some error","Error":e.args})