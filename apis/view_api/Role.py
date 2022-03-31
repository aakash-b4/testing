from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from apis.view_api.beneficiary import merchantFetchBeneficiary
from ..serializersFolder.serializers import LogsSerializer
#from .serializers import *
# from .models import *
import ast
from ..other_service import payout_service
from ..database_models import RoleModel
from apis.database_service.Ledger_model_services import *
from django.http.response import JsonResponse
from apis.other_service.enquiry_service import *
from apis.database_service.Beneficiary_model_services import *
from ..database_service import Role_model_service
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

from datetime import datetime, time

from ..other_service import login_service,signup_service

from rest_framework.response import *
from sabpaisa import auth

class addRole(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="add Role request at "+request.path+" slug",
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
            service = Role_model_service.Role_Model_service(role_name = query.get("role_name"),permited_apis=query.get("permited_apis"))
            resp = service.save(admin_id=adminId,client_ip_address=request.META['REMOTE_ADDR'])
            if(resp==0):
                return Response({"message":"duplicate data found","response_code":"0"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"data saved","response_code":"1"},status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})


class fetchRoles(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="add Role request at "+request.path+" slug",
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
            
            service = Role_model_service.Role_Model_service()
            resp = service.fetchRoles(admin_id=adminId,client_ip_address=request.META['REMOTE_ADDR'])
            if(resp==0):
                return Response({"message":"data found","data":None,"response_code":"0"},status=status.HTTP_404_NOT_FOUND)
            return Response({"message":"data found","data":resp,"response_code":"1"},status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})

class deleteRole(APIView):
    def post(self,request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="add Role request at "+request.path+" slug",
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
            service = Role_model_service.Role_Model_service()
            resp = service.deleteRole(admin_id=adminId,client_ip_address=request.META['REMOTE_ADDR'],role_name = query.get("role_name"))
            return Response({"message":"data deleted successfully","response_code":"1"},status=status.HTTP_201_CREATED)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            Log_model_services.Log_Model_Service.update_response(logid,{"message":"Some error occured","Error_Code":e.args,"response_code":"2"})
            return Response({"Message":"some error","Error":e.args})
