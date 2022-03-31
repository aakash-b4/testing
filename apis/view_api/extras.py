# from django.shortcuts import render
# Create your views here.


from apis.database_service import Merchant_mode_services
from apis.database_service.Merchant_mode_services import Merchant_Mode_Service
from apis.database_models.MerchantModeModel import MercahantModeModel
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

from apis.database_service import Beneficiary_model_services, Mode_model_services
from ..API_docs import payout_docs,auth_docs,login_docs,payoutTransactionEnquiry_docs,addBalance_docs,addBeneficiary_docs,log_docs,ledgers_docs
from datetime import datetime
from ..serializersFolder.serializers import LogsSerializer
#from .serializers import *
# from .models import *
import ast
from ..other_service import payout_service
from ..database_models import LedgerModel,ModeModel,BankModel
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

import ast
from sabpaisa import auth


class encryptJSON(APIView):
    def post(self, request):
        query = str(request.data.get("query"))
        authKey = request.data.get("authkey")
        authIV = request.data.get("authiv")
        encResp = auth.AESCipher(authKey,authIV).encrypt(query)
        print(".............. ",encResp)
        return Response({"message": "data", "data": str(encResp), "response_code": "3"}, status=status.HTTP_200_OK)

class decryptJson(APIView):
    def post(self,request):
        query = request.data.get("query")
        authKey = request.data.get("authkey")
        authIV = request.data.get("authiv")
        encResp = auth.AESCipher(authKey,authIV).decrypt(query)
        return Response({"message": "data", "data": str(encResp), "response_code": "3"}, status=status.HTTP_200_OK)
class fetch(APIView):
    #permission_classes = (IsAuthenticated, )
    @swagger_auto_schema(request_body=ledgers_docs.fetch_request,responses=ledgers_docs.fetch_response_dict)
    def post(self,request,page,length):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="Post request at "+request.path+" slug", table_name="apis_ledgermodel",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = request.headers["auth_token"]
        if(resp == ""):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "3"})
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        if page == "all" and length != "all":
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "page and length format does not match", "response_code": "3"})
            return JsonResponse({"Message": "page and length format does not match", "data": None, "response_code": "3"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if(int(page)!= 1 and length == "all"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "page and length format not compatible", "response_code": "3"})
            return JsonResponse({"Message": "page and length format not compatible", "data": None, "response_code": "3"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if(resp == ""):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "merchant code missing", "response_code": "3"})
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(resp)
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=decMerchant, created_by="merchant id :: "+decMerchant, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        # query=None
        print("request :: ",request.data)
        if(request.data.get("query")!=None):
            query = auth.AESCipher(authKey,authIV).decrypt(request.data.get("query")).split("'")
            key = query[1]
            value = query[3]
        clientCode = None
        customer_ref_no = None
        trans_type=None
        startTime=None
        endTime = None
        balance = Ledger_Model_Service.getBalance(decMerchant,request.META['REMOTE_ADDR'],"merchant id :: "+decMerchant)
        if(clientModel.is_encrypt== False):
            print("hellllllllllllo")
            startTime = request.data.get("startTime")
            endTime= request.data.get("endTime")
            clientCode=request.data.get("clientCode")
            customer_ref_no=request.data.get("orderId")
            trans_type=request.data.get("trans_type")
        else:
            print("yoooooo")
            print(query)
            if(len(query)>5):
                customer_ref_no=query[3]
                trans_type=query[7]
                clientCode=query[11]
            elif(key=="startTime"):
                startTime = value
                if(query[5]=="endTime"):
                    endTime=query[7]
            elif(key=="clientCode"):
                clientCode = value
            elif(key=="orderId"):
                customer_ref_no = value
            elif(key=="trans_type"):
                trans_type = value
        resp = enquiry_service.fetchLedgerByParams(client_code = clientCode,
        startTime=startTime,endTime=endTime,page=page,length=length,
        merchant = decMerchant,customer_ref_no=customer_ref_no,trans_type=trans_type,created_by="merchant id :: "+decMerchant,client_ip_address=request.META['REMOTE_ADDR'])
        if(resp=="-2"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "length of page is greater then the result length", "response_code": "2"})
            return Response({"message": "length of page is greater then the result length", "data": None, "response_code": "2"}, status=status.HTTP_404_NOT_FOUND)

        if(resp=="0"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "no data for the given credentials", "response_code": "2"})
            return Response({"message": "no data for the given credentials", "data": None, "response_code": "2"}, status=status.HTTP_404_NOT_FOUND)
        if(resp=="-1"):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "missing mandatory parameters", "response_code": "3"})
            return Response({"message": "missing mandatory parameters", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        result = list()
        if(len(resp)>0):
            for r in resp:
                res = { 
                        "id":r.get("id"),
                        'payoutTransactionId':r.get("payout_trans_id"),
                        'amount': r.get("amount"),
                        'transType': r.get("trans_type"),
                        'statusType': r.get("type_status"),
                        'bankRefNo': r.get("bank_ref_no"),
                        'orderId': r.get("customer_ref_no"),
                        'beneficiaryAccountName': r.get("bene_account_name"),
                        'beneficiaryAccountNumber': r.get("bene_account_number"),
                        'beneficiaryIFSC': r.get("bene_ifsc"),
                        'transStatus': r.get("trans_status"),
                        'mode': r.get("mode"),
                        'trans_amount_type':r.get("trans_amount_type")
                    }
                result.append(res)
        encResp = {
            "balance":balance,
            "data":result
        }
        encResult = auth.AESCipher(authKey,authIV).encrypt(str(encResp))
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": str(resp), "response_code": "1"})
        return Response({"message": "data found", "data": encResp, "response_code": "1"}, status=status.HTTP_200_OK)
class tester(APIView):
    def get(self,request):
        authKey = const.AuthKey
        authIV = const.AuthIV
        resp = request.headers["merchant"]
        decMerchant = auth.AESCipher(authKey, authIV).decrypt(resp)
        return Response({"header": decMerchant, "authkey": authKey, "authIV": authIV})


class bankApiEnquiryView(APIView):
    @swagger_auto_schema()
    def post(self,req):
        pass


class bankFilter(APIView):
    def get(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetch modes request at "+request.path+" slug",
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
            
            resp = BankModel.BankPartnerModel.objects.filter().all().values()
            if(len(resp)==0):
                return Response({"message":"no data found","data":None,"response_code":"0"},status=status.HTTP_404_NOT_FOUND)
            response =  list()
            for data in resp:
                dict = {
                    "bank_id":data.get("id"),
                    "bank_name":data.get("bank_name"),
                    "bank_code":data.get("bank_code")
                }
                response.append(dict)
            if(admin.is_encrypt==True):
                encResp = auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(response))
                return Response({"message":"data found","data":encResp},status=status.HTTP_200_OK)  
            
            return Response({"message":"data found","data":response},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
           
    
class AllMode(APIView):
    def get(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetch modes request at "+request.path+" slug",
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
            
            response = Mode_model_services.Mode_Model_Service.fetchAllMerchant()
            
            if(response==-1):
                return Response({"message":"data not found","data":None,"response_code":"0"},status=status.HTTP_404_NOT_FOUND)
            if(admin.is_encrypt==True):
                encResp = auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(response))
                return Response({"message":"data found","data":encResp})  
            return Response({"message":"data found","data":response,"response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

class MerchantModes(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetch merchants modes request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        try:
            query = request.data.get("query")
            header = request.headers.get("auth_token")
            adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
            admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
            if(admin==None):
                Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
                return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
            if(admin.is_encrypt==True):
                decRequest = auth.AESCipher(admin.auth_key,admin.auth_iv).decrypt(query)
                # merchantId = decRequest.get("merchant_id")
                merchantId = ast.literal_eval(decRequest)
                merchantId = merchantId.get("merchant_id")   
            else:
                merchantId = query.get("merchant_id")
            
            merchantId = auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(str(merchantId))
            resp = Merchant_mode_services.Merchant_Mode_Service.fetchModesByMerchantId(merchantId)
            if(len(resp)==0):
                return Response({"message":"data not found","data":None,"response_code":'0'},status=status.HTTP_404_NOT_FOUND)    
            if(admin.is_encrypt==True):
                encResp = auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(resp))
                return Response({"message":"data found","data":encResp,"response_code":'1'},status=status.HTTP_200_OK)    
            return Response({"message":"data found","data":resp,"response_code":'1'},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})


class tax(APIView):
    def get(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetchCharges request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        header = request.headers.get("auth_token")
        adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
        admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
        if(admin==None):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
            return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
        resp = TaxModel.objects.filter(status=True).values()
        if(len(resp) == 0):
            print("len = 0")
            return Response({"message":"data not found","data":None, "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
        resp = resp[0].get("tax")
        if(admin.is_encrypt==True):
                encResp = auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(resp))
                return Response({"message":"data found","data":encResp,"response_code":'1'})    
        return Response({"message":"data found","data":resp,"response_code":'1'},status=status.HTTP_200_OK)

class AddTax(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetchCharges request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        header = request.headers.get("auth_token")
        adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
        admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
        if(admin==None):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
            return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
        query = request.data.get("query")
        
        tax=TaxModel()
        tax.tax=query.get("tax")
        resp = TaxModel.objects.filter(tax=tax.tax,status=True)
        if(len(resp)!=0):
            return Response({"message":"tax already active","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
        startTranstime=query.get("start_date")
        startYear = int(startTranstime[0:4])
        startMonth = int(startTranstime[5:7])
        startDay = int(startTranstime[8:10])
        startHours = int(startTranstime[11:13])
        startMinute = int(startTranstime[14:16])
        dt = datetime.now()
        start = dt.replace(year=startYear, day=startDay, month=startMonth, hour=startHours, minute=startMinute, second=0, microsecond=0)
        tax.start_date=start
        tax.created_by="admin ID :: "+str(adminId)
        tax.save()
        return Response({"message":"data saved","response_code":"1"},status=status.HTTP_201_CREATED)

class UpdateTax(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fetchCharges request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        header = request.headers.get("auth_token")
        adminId = auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(header)
        admin = BO_user_services.BO_User_Service.fetch_by_id(adminId)
        if(admin==None):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "admin code missing", "response_code": "0"})
            return Response({"message":"admin id does not exist", "Response code":"0"},status=status.HTTP_404_NOT_FOUND)
        query = request.data.get("query")
        
        
        tax_query=query.get("tax")
        resp = TaxModel.objects.filter(tax=tax_query,status=True)
        if(len(resp)==0):
            return Response({"message":"tax does not exist","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
        end_date = query.get("end_date")
        endYear = int(end_date[0:4])
        endMonth = int(end_date[5:7])
        endDay = int(end_date[8:10])
        endHours = int(end_date[11:13])
        endMinute = int(end_date[14:16])
        dt = datetime.now()
        end = dt.replace(year=endYear, day=endDay, month=endMonth, hour=endHours, minute=endMinute, second=0, microsecond=0)
        resp[0].end_date=end
        resp[0].status = False
        resp[0].updated_on=datetime.now()
        resp[0].updated_by = "admin ID :: "+str(adminId)
        resp[0].save()
        return Response({"message":"data updated","response_code":"1"},status=status.HTTP_200_OK)