# from django.shortcuts import render
# Create your views here.


import threading
from apis.other_service.ledger_service import Ledger_service
from django.db.models import query
from time import sleep

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
from datetime import datetime, time
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
from ..database_service.BO_user_services import BO_User_Service
# from 

from sabpaisa import auth

import mimetypes
class GetLedgerForMerchant(APIView):
    def get(self,req):
        try:
            auth_token = req.headers["auth_token"]
            id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            if Client_model_service.Client_Model_Service.fetch_by_id(id,req.META['REMOTE_ADDR'],"merchant :: "+str(id))==None:
                return Response({"message":"user not valid","response_code":"0"})
            data=Ledger_service(id,req.META['REMOTE_ADDR'],"merchant :: "+str(id)).getLedgerForMerchant()
            
            return Response({"message":"date found","data":data,"response_code":"1"})
        except Exception as e:
         import traceback
         print(traceback.format_exc())
        #  Log_model_services.Log_Model_Service.update_response(logid,{"Message":e.args,"response_code":"2"})
         return Response({"Message":"Some Technical error","response_code":"2"},status=status.HTTP_204_NO_CONTENT)

class GetLedger(APIView):
    def post(self,req,page,length):
        try:
            auth_token = req.headers["auth_token"]
            id=auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(auth_token)
            if BO_User_Service.fetch_by_id(id)==None:
                return Response({"message":"user not valid","response_code":"0"})
            data=Ledger_Model_Service.getLedgers(page,length,req.META['REMOTE_ADDR'],"Admin Id :: "+str(id))
            
            return Response({"message":"date found","data":data,"response_code":"1"})
        except Exception as e:
         import traceback
         print(traceback.format_exc())
        #  Log_model_services.Log_Model_Service.update_response(logid,{"Message":e.args,"response_code":"2"})
         return Response({"Message":"Some Technical error","response_code":"2"},status=status.HTTP_204_NO_CONTENT)
class GetTransactionHistory(APIView):
    def post(self,req,page,length):
        try:
            auth_token = req.headers["auth_token"]
            start_date=req.data["start"]
            end_date=req.data['end']
            trans_amount_type=req.data['transfer_type']
            trans_status=req.data['trans_status']
            if start_date!="all":
                start_date=datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            if end_date!='all':
                end_date=datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            if Client_model_service.Client_Model_Service.fetch_by_id(id,req.META['REMOTE_ADDR'],"Merchant Id :: "+str(id))==None:
                return Response({"message":"user not valid","response_code":"0"})
            # data=Ledger_Model_Service.getLedgers(page,length,req.META['REMOTE_ADDR'],"Admin Id :: "+str(id))
            data=Ledger_Model_Service.getTransactionHistory(page,length,start_date,end_date,id,trans_amount_type,trans_status)
            return Response({"message":"date found","data":data,"response_code":"1"})
        except Exception as e:
         import traceback
         print(traceback.format_exc())
         #  Log_model_services.Log_Model_Service.update_response(logid,{"Message":e.args,"response_code":"2"})
         return Response({"Message":"Some Technical error","response_code":"2"},status=status.HTTP_204_NO_CONTENT)
class LedgerSaveRequest(APIView):
    #permission_classes = (IsAuthenticated, )
    def post(self,request):
        # print(request.data.get("client"))
        merchant= request.data.get("merchant")
        query = request.data.get("query")
        ip = request.data.get("client_ip_address")
        createdBy = request.data.get("created_by")
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=createdBy, client_ip_address=ip)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey, authIV).decrypt(query)
        res = ast.literal_eval(encResp)
        print("res......... ", res)
        print(type(res))
        service = Ledger_Model_Service(
            trans_amount_type=res.get("trans_amount_type"),
            merchant=res.get("merchant"),
            client_code=res.get("client_code"),
            type_status=res.get("type_status"),
            amount=res.get("amount"),
            van=res.get("van"),
            trans_type=res.get("trans_type"),
            trans_status=res.get("trans_status"),
            bank_ref_no= res.get("bank_ref_no"),
            customer_ref_no= res.get("customer_ref_no"),
            bank_id=res.get("bank"),
            trans_time=datetime.now(),
            bene_account_name=res.get("bene_account_name"),
            bene_account_number=res.get("bene_account_number"),
            bene_ifsc=res.get("bene_ifsc"),
            request_header=res.get("request_header"),
            mode =  res.get("mode"),
            charge = res.get("charge"),
            createdBy=res.get("createdBy"),
            updatedBy=res.get("updatedBy"),
            deletedBy=res.get("deletedBy"),
            created_at=datetime.now()
                                       )
        resp = service.save(client_ip_address=ip,
                            merchant=merchant, createdBy=createdBy)
        if(resp == "0"):
            return Response({"message": "nothing to show", "data": None, "response_code": "0"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "data found", "data": resp, "response_code": "1"}, status=status.HTTP_200_OK)
        
class DeleteLedger(APIView):
    #permission_classes = (IsAuthenticated, )
    def delete(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        
        log = Log_model_services.Log_Model_Service(log_type="Delete request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        id = request.data.get("id")
        deletedBy = request.data.get("deletedBy")
        m = request.headers["merchant"]
        aKey = const.AuthKey
        aIV = const.AuthIV
        merchant = auth.AESCipher(aKey, aIV).decrypt(m)
        print("id===== ",id)
        resp = Ledger_Model_Service.deleteById(
            id, deletedBy, merchant, request.META['REMOTE_ADDR'], deletedBy)

        if(resp == True):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "delete successfully", "response_code": "1"})
            return JsonResponse({"Message": "delete successfully","response_code": "1"}, status=status.HTTP_200_OK)
        else:
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "Id not found", "response_code": "2"})
            return JsonResponse({"Message": "Id not found", "response_code": "2"}, status=status.HTTP_404_NOT_FOUND)

class UpdateLedger(APIView):
    #permission_classes = (IsAuthenticated, )
    def put(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        m = request.headers["merchant"]
        if(m == ""):
            return Response({"message": "merchant code missing", "data": None, "response_code": "3"}, status=status.HTTP_400_BAD_REQUEST)
        aKey = const.AuthKey
        aIV = const.AuthIV
        merchant = auth.AESCipher(aKey, aIV).decrypt(m)
        query = request.data.get("query")
        createdBy = request.data.get("created_by")
        log = Log_model_services.Log_Model_Service(log_type="update request at "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const.server_ip, full_request=request_obj)
        logid = log.save()
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=createdBy, client_ip_address=request.META['REMOTE_ADDR'])
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        encResp = auth.AESCipher(authKey, authIV).decrypt(query)
        res = ast.literal_eval(encResp)
        id = res.get("id")
        ledger = LedgerModel.objects.filter(id=id,merchant=merchant,status=True)
        if(len(ledger) ==  0):
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": res, "response_code": "0"})
            return JsonResponse({"Message": "id or merchantcode or status miss matched", "response_code": "0"}, status=status.HTTP_404_NOT_FOUND)
        if(len(ledger) > 0):
            ledgermodel = ledger[0]
            d = ledger[0].created_at
            service = Ledger_Model_Service(
                id=request.data.get("id"),
                trans_amount_type=res.get("trans_amount_type"),
                merchant=res.get("merchant"),
                client_code=res.get("client_code"),
                type_status=res.get("type_status"),
                amount=res.get("amount"),
                van=res.get("van"),
                trans_type=res.get("trans_type"),
                trans_status=res.get("trans_status"),
                bank_ref_no=res.get("bank_ref_no"),
                customer_ref_no=res.get("customer_ref_no"),
                bank_id=res.get("bank"),
                trans_time=datetime.now(),
                bene_account_name=res.get("bene_account_name"),
                bene_account_number=res.get("bene_account_number"),
                bene_ifsc=res.get("bene_ifsc"),
                request_header=res.get("request_header"),
                mode=res.get("mode"),
                charge=res.get("charge"),
                created_at=d,
                # deleted_at=ledgermodel.deleted_at,
                createdBy=res.get("createdBy"),
                updatedBy=res.get("updatedBy"),
                updated_at=datetime.now()
            )
            Log_model_services.Log_Model_Service.update_response(
                logid, {"Message": "updated successfully", "response_code": "1"})
            res = service.update(id=id, merchant=merchant,
                                 client_ip_address=request.META['REMOTE_ADDR'], created_by=createdBy)
            return JsonResponse({"Message": "updated successfully", "response_code": "1"}, status=status.HTTP_200_OK)
        Log_model_services.Log_Model_Service.update_response(
            logid, {"Message": "something went wrong!!!!", "response_code": "0"})
        return JsonResponse({"Message": "something went wrong!!!!", "response_code": "0"}, status=status.HTTP_400_BAD_REQUEST)

class fetchInfo(APIView):
    def get(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="fecth info request at "+request.path+" slug",
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
            response = Ledger_Model_Service.fetchInfo()
            if(admin.is_encrypt==True):
                encResp = auth.AESCipher(admin.auth_key,admin.auth_iv).encrypt(str(response))
                return Response({"message":"data found","data":encResp,"response_code":"1"},status=status.HTTP_200_OK) 
            return Response({"message":"data found","data":response,"response_code":"1"})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

class CreditDebitBalanceInfo(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)
        log = Log_model_services.Log_Model_Service(log_type="CreditDebitBalanceInfo info request at "+request.path+" slug",
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
                merchant_id= query.get("merchant_id")
                if(merchant_id=="all"):
                    response = Ledger_Model_Service.AllCreditDebit(merchant_id=merchant_id,created_by="admin ID :: "+str(adminId),client_ip_address=request.META['REMOTE_ADDR'])
                else:
                    response = Ledger_Model_Service.merchantCreditDebit(merchant_id=merchant_id,created_by="admin ID :: "+str(adminId),client_ip_address=request.META['REMOTE_ADDR'])
                
                return Response({"message":"data found","data":response,"response_code":"1"})
        except Exception as e:
                import traceback
                print(traceback.format_exc())
                Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
                return Response({"Message":"some error","Error":e.args})

from django.views.decorators.csrf import csrf_exempt


class DownloadExcelView(APIView):
    @csrf_exempt
    def get(self,req,page,length):
        try:
            print(req.GET)
            auth_token = req.GET.get("auth_token")
            start_date=req.GET.get("start")
            end_date=req.GET.get('end')
            trans_amount_type=req.GET.get('transfer_type')
            trans_status=req.GET.get('trans_status')
            if start_date!="all" or end_date!='all':
                start_date=datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                end_date=datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            id=auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            if Client_model_service.Client_Model_Service.fetch_by_id(id,req.META['REMOTE_ADDR'],"Merchant Id :: "+str(id))==None:
                return Response({"message":"user not valid","response_code":"0"})
            # data=Ledger_Model_Service.getLedgers(page,length,req.META['REMOTE_ADDR'],"Admin Id :: "+str(id))
            data=Ledger_Model_Service.getTransactionHistory(page,length,start_date,end_date,id,trans_amount_type,trans_status)
            

            import csv
            import os
            filename=str(datetime.now()).replace(" ","").replace("-","").replace(".","").replace(":","")+".csv"
            f=open(filename,"w",newline="")
            op=csv.writer(f)
            # {}.
            
            if len(data["data"])>0:
                op.writerow(list(data["data"][0].keys()))
            for i in data["data"]:
            
                op.writerow(list(i.values()))
            
            class DeleteThreading(threading.Thread):
                def run(self):
                    sleep(10)
                    print("running thread")
                    if os.path.exists(filename):
                         os.remove(filename) 
            DeleteThreading().start()
            # if os.path.exists(filename):
            #     os.remove(filename)
            
            # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # filepath = BASE_DIR + filename
            read=open(filename,"rb")
            
            # mime_type, _ = mimetypes.guess_type(filepath)
           
            response=FileResponse(read,as_attachment=True)
            # read.close()
            f.close()
    #         response=HttpResponse(
    #            read,
    #     content_type="application/force-download",
    #     headers={'Content-Disposition': 'attachment; filename="'+filename+'"'},
    # )
            return response
            # return Response({"message":"date found","data":data,"response_code":"1"})
        except Exception as e:
         import traceback
         print(traceback.format_exc())
         #  Log_model_services.Log_Model_Service.update_response(logid,{"Message":e.args,"response_code":"2"})
         return Response({"Message":"Some Technical error","response_code":"2"},status=status.HTTP_204_NO_CONTENT)