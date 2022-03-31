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
from ..serializersFolder.serializers import DailyLedgerSerializer, LogsSerializer
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
# from ..bank_services import ICICI_service


from ..database_service.DailyLedger_model_services import DailyLedger_Model_Service


class DailyLedgerViewApi(APIView):
    def get(self,req):
        try:
            DailyLedger_Model_Service.callDailyLedger()
            return Response({"message":"Daily Ledger Called","response_code":1},status=status.HTTP_200_OK)
        except Exception as e:
             import traceback
             print(traceback.format_exc())
             return Response({"message":"Some Error","response_code":0},status=status.HTTP_400_BAD_REQUEST)



class MISViewApi(APIView):
    def get(self,req,page,length,start,end):
        try:
            auth_token = req.headers["auth_token"]
            
            if auth_token=="all":
                merchant_id="merchant_id"
            else:
                merchant_id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            
            # if start!="all" or end!='all':
                
            #     start=date.strftime(start, "%Y-%m-%d")
            #     end=date.strftime(end, "%Y-%m-%d")
            dailyledger=DailyLedger_Model_Service.fetch(page,length,merchant_id,start,end)
            # if dailyledger==None:
            #     return Response({"message":"data not found","response_code":0})
            # dailyledgersel=DailyLedgerSerializer(dailyledger,many=True)
            
            return Response({"message":"data found","data":dailyledger,"response_code":1})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"message":"some technical error","response_code":2},status=status.HTTP_400_BAD_REQUEST)