from apis.other_service.ledger_service import Ledger_service
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
from ..database_service import Client_model_service
from rest_framework.parsers import JSONParser
from ..database_service import Client_model_service,IpWhitelisting_model_service
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

from ..other_service import login_service,signup_service
from ..database_service.BO_user_services import BO_User_Service
# from 

from sabpaisa import auth
from ..database_service.Bank_model_services import Bank_model_services

class BankPartnerApiSave(APIView):
    def post(self,req):
        try:
            data=req.data
            bankModel=Bank_model_services.fetch_by_bankcode(data["bank_code"],req.META['REMOTE_ADDR'],"system")
            if bankModel!=None:
                return Response({"message":"bank code already exist","responseCode":0})
            bank=Bank_model_services(bank_name=data["bank_name"],bank_code=data["bank_code"],nodal_account_name=data["nodal_account_name"],nodal_ifsc=data["nodal_ifsc"],nodal_account_number=data["nodal_account_number"])
            bank.save(req.META['REMOTE_ADDR'],"system")
            return Response({"message":"bank added","responseCode":1})
        except Exception as e:
            bankModel=Bank_model_services.fetch_by_bankcode(data["bank_code"],req.META['REMOTE_ADDR'],"system")
            if bankModel!=None:
                bankModel.delete()
            return Response({"message":"some error","responseCode":2})

class ChargeBreakUpInfoApi(APIView):
    def post(self,request,length,page):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="fetch ChargeBreakUpInfoApi request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            header = request.headers.get("auth_token")
            adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if(admin==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin id does not exist", "response_code": "0"})
                return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            query=request.data.get("query")
            payoutMode = query.get("payment_mode")
            bankMode = query.get("bank_name")
            start_date = query.get("start_date")
            end_date = query.get("end_date")
            if start_date !="all":
                start_date=datetime.strptime(start_date, "%Y-%m-%d")                    
            if end_date!='all':
                end_date=datetime.strptime(end_date, "%Y-%m-%d")
            resp = Bank_model_services.ChargeBankInfo(payoutMode=payoutMode,bank_name=bankMode,page=page,length=length,start=start_date,end=end_date)
            if(resp == -1):
                return Response({"message":"data","data":None,"response_code":"0"},status=status.HTTP_404_NOT_FOUND)
            return Response({"message":"data","data":resp,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})
