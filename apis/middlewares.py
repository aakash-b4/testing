from apis.database_models.ClientModel import MerchantModel
import requests
from apis.database_models.IpWhiteListedModel import IpWhiteListedModel
from apis.database_service.Client_model_service import Client_Model_Service
from apis.database_service.BO_user_services import BO_User_Service
from apis.database_service.UserActive_model_service import UserActive_Model_Service
from apis.models import RoleModel
from . import models
from rest_framework.response import *
from django.shortcuts import HttpResponse
from datetime import datetime, timedelta, timezone
from sabpaisa import auth
import logging
import pytz
# from .database_service.Log_model_services import Log_Model_Service
from . import const

logger = logging.getLogger("info_logger")

def IpWhiteListed(get_response):
    def middleware(request):
        print(request.headers)
        ip = request.META['REMOTE_ADDR']
        try:
            if(request.path != "/api/" and request.path != "/chargeBreakUpInfo/" and request.path != "/api/addCharge/" and request.path != "/" and "/admin/" not in request.path and request.path != "/api/signup/" and request.path not in "/api/token/" and request.path != "/api/loginrequest/" and request.path != "/api/loginverified/" and request.path != "/api/resendotp/" and request.path != "/api/adminLogin/" and request.path != "/api/adminSignup/" and request.path != "/api/addSlab/" and "/api/getLedgers/" not in request.path and "/api/getTransactionHistory/" not in request.path and request.path != "/api/addBalance/" and "/api/getAllMerchants/" not in request.path and "/api/getLogs/" not in request.path and request.path != "/api/todayInfo/" and request.path != "/api/callDailyLedger/" and request.path != "/api/getTax/" and request.path != "/api/allModes/" and request.path != "/api/bankPartnerInfo/" and request.path != "/api/saveBankPartner/" and "/api/fetchBeneficiaryfor/" not in request.path and request.path != "/api/saveBeneficiaryfor/" and "/api/creditamountmis/" not in request.path and "/api/downloadExcelLedger/" not in request.path and const.merchant_check):
                if "api_key" not in request.headers:
                    print("not condition")
                    error_res = HttpResponse(
                        str({"message": "APIKEY not provided"}))
                    error_res['Content-Type'] = 'application/json'
                    return error_res

                merchant_id = request.headers["auth_token"]
                merchant_id = auth.AESCipher(
                    const.AuthKey, const.AuthIV).decrypt(merchant_id)
                print(merchant_id)
                clientmodel = Client_Model_Service.fetch_by_id(
                    int(merchant_id), request.META['REMOTE_ADDR'], merchant_id)
                bomodel = BO_User_Service.fetch_by_id(merchant_id)
                if not (clientmodel or bomodel):
                    error_res = HttpResponse(
                        str({"message": "user not valid"}))
                    error_res['Content-Type'] = 'application/json'
                    return error_res
                if "/api/getLogs/" in request.path:
                    pass
                if not clientmodel.is_ip_checking:
                    response = get_response(request)
                    # response["Access-Control-Allow-Origin"] = "*"
                    # response["Access-Control-Allow-Headers"] = "*"
                    return response
                ipWhiteListedModel = models.IpWhiteListedModel.objects.filter(
                    ip_address=ip, status=True, merchant=merchant_id)
            else:
                ipWhiteListedModel = models.IpWhiteListedModel.objects.filter(
                    ip_address=ip, status=True)

        except Exception as e:
            error_res = HttpResponse(str({"message": e.args}))
            error_res['Content-Type'] = 'application/json'
            return error_res
        print("request -->>", request.path)
        if len(ipWhiteListedModel) == 0 and const.ipwhitelisting:
            iprecords = models.IpHittingRecordModel()
            iprecords.ip_address = ip
            iprecords.ip_type = "Blocked"
            iprecords.hitting_time = datetime.now()
            iprecords.save()
            ip_res = HttpResponse(str({"message": "IP Not Authorized"}))
            ip_res['Content-Type'] = 'application/json'
            return ip_res
        # iprecords=models.IpHittingRecordModel()
        # iprecords.ip_address=ip
        # iprecords.ip_type="Allowed"
        # iprecords.hitting_time=datetime.now()
        # iprecords.save()

        response = get_response(request)
        # response["Access-Control-Allow-Origin"] = "*"
        # response["Access-Control-Allow-Headers"] = "*"
        # print(response)
        return response
    return middleware
# def Logs(get_response):
#     def middleware(req):
#         client_ip=req.META['REMOTE_ADDR']
#         server_ip = const.server_ip
#         request = request.__dic__
#         Log_Model_Service()
#         response = get_response(req)
#         return response
#     return middleware


def MultiTabsRestriction(get_response):
    def middleware(req):

        if req.path != "/api/" and req.path != "/" and "/admin/" not in req.path and req.path != "/api/signup/" and req.path not in "/api/token/" and req.path != "/api/loginrequest/" and req.path != "/api/loginverified/" and req.path != "/api/resendotp/" and req.path != "/api/adminLogin/" and req.path != "/api/adminSignup/" and const.multitabs:

            merchant_id = req.headers["auth_token"]
            tab_token = req.headers["tab_token"]
            login_token = req.headers['login_token']
            ip = req.META['REMOTE_ADDR']
            logged_in_active_users = UserActive_Model_Service.check_active_user(
                login_token=login_token, tab_token=tab_token)
            if len(logged_in_active_users) > 0:
                res = HttpResponse(
                    str({"message": "Already active on some other tab on some other device"}))
                res['Content-Type'] = 'application/json'
                return res
            merchant_id = auth.AESCipher(
                const.AuthKey, const.AuthIV).decrypt(merchant_id)
            user_active = UserActive_Model_Service.fetch_by_merchant_id(
                merchant_id)
            # last_login_time=user_active.last_server_call_time
            # login_expire = user_active.login_expire_time
            now = datetime.now(pytz.timezone('Asia/Kolkata'))
            # now.replace(tzinfo=timezone.utc)
            if user_active.client_ip_address != ip and user_active.login_status == "active":
                res = HttpResponse(str({"message": "ip does not matched"}))
                res['Content-Type'] = 'application/json'
                return res
            elif user_active.active_status == "active" and tab_token != user_active.tab_token and user_active.login_status == "active" and user_active.tab_token_expire_time > now and user_active.login_expire_time > now:
                res = HttpResponse(
                    str({"message": "Already active on some other tab"}))
                res['Content-Type'] = 'application/json'
                return res
            elif user_active.active_status == "active" and user_active.login_status == "active" and user_active.login_expire_time <= now:
                UserActive_Model_Service.update_active_status(
                    user_active.id, "Not_active")
                res = HttpResponse(
                    str({"message": "Please Login to payout first"}))
                res['Content-Type'] = 'application/json'
                return res
            elif user_active.active_status != "active" and user_active.login_status == "active" or user_active.login_expire_time > now:
                UserActive_Model_Service.recreate_tab_token(user_active.id)
                UserActive_Model_Service.update_login_exipre(
                    user_active.id, datetime.now()+timedelta(days=3))
                res = get_response(req)
                return res
            elif user_active.active_status == "active" and user_active.tab_token_expire_time <= now and user_active.login_status == "active" or user_active.login_expire_time > now:
                UserActive_Model_Service.recreate_tab_token(user_active.id)
                UserActive_Model_Service.update_login_exipre(
                    user_active.id, datetime.now()+timedelta(days=3))
                res = get_response(req)
                return res
            elif user_active.login_status != "active" or user_active.login_expire_time <= now:
                res = HttpResponse(
                    str({"message": "Please Login to payout first"}))
                res['Content-Type'] = 'application/json'
                return res

            if user_active.active_status == "active" and tab_token == user_active.tab_token and user_active.tab_token_expire_time <= now and user_active.login_expire_time > now:
                UserActive_Model_Service.update_login_exipre(
                    user_active.id, datetime.now()+timedelta(days=3))
                UserActive_Model_Service.update_tab_exipre(
                    user_active.id, datetime.now()+timedelta(hours=1))
                res = get_response(req)
                return res

            UserActive_Model_Service.update_tab_exipre(
                user_active.id, datetime.now()+timedelta(hours=1))
            res = get_response(req)
            # res["Access-Control-Allow-Origin"] = "*"
            # res["Access-Control-Allow-Headers"] = "*"

            return res
        res = get_response(req)
        # res["Access-Control-Allow-Origin"] = "*"
        # res["Access-Control-Allow-Headers"] = "*"
        return res

    return middleware


def checkClientStatus(get_response):
    def middleware(req):
        print(req.path)

        if req.path != "/api/" and req.path != "/api/deleteCharge/" and req.path != "/api/updateCharge/" and req.path != "/api/chargeBreakUpInfo/" and req.path != "/api/addCharge/" and req.path != "/" and "/admin/" not in req.path and req.path != "/api/signup/" and req.path not in "/api/token/" and req.path != "/api/loginrequest/" and req.path != "/api/loginverified/" and req.path != "/api/resendotp/" and req.path != "/api/adminLogin/" and req.path != "/api/adminSignup/" and req.path != "/api/addSlab/" and "/api/getLedgers/" not in req.path and "/api/getTransactionHistory/" not in req.path and req.path != "/api/addBalance/" and "/api/getAllMerchants/" not in req.path and "/api/getLogs/" not in req.path and req.path != "/api/todayInfo/" and req.path != "/api/callDailyLedger/" and req.path != "/api/getTax/" and req.path != "/api/allModes/" and req.path != "/api/bankPartnerInfo/" and req.path != "/api/saveBankPartner/" and "/api/fetchBeneficiaryfor/" not in req.path and req.path != "/api/saveBeneficiaryfor/" and "/api/creditamountmis/" not in req.path and "/api/downloadExcelLedger/" not in req.path and req.path != "/api/modesByMerchantId/" and "/api/chargeBreakUpInfo/" not in req.path and req.path != "/api/UpdateMerchantModeStatus/" and req.path != "/api/addMerchantMode/" and "/api/fetchCharges/" not in req.path and req.path != "/api/fetchSlab/" and req.path != "/api/updateSlab/" and req.path != "/api/deleteSlab/" and req.path != "/api/merchantsignup/" and req.path != "/api/testicici/":
            print("inside if")
            try:
                merchant_id = req.headers["auth_token"]

                merchant_id = auth.AESCipher(
                    const.AuthKey, const.AuthIV).decrypt(merchant_id)
                clientmodel = Client_Model_Service.fetch_by_id(
                    int(merchant_id), req.META['REMOTE_ADDR'], merchant_id)
                print(merchant_id)
                if clientmodel is None:
                    print('enter if')
                    error_res = HttpResponse(
                        str({"message": "user not valid"}))
                    error_res['Content-Type'] = 'application/json'
                    return error_res
                elif not clientmodel.status:
                    logger.info("user not active")
                    error_res = HttpResponse(
                        str({"message": "user not active"}))
                    error_res['Content-Type'] = 'application/json'
                    return error_res
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                error_res = HttpResponse(str({"message": e.args}))
                error_res['Content-Type'] = 'application/json'
                return error_res
        res = get_response(req)
        return res
    return middleware


def checkBackofficeStatus(get_response):
    def middleware(req):
        if req.path != "/api/" and req.path != "/api/addBeneficiaries/" and req.path != "/" and "/admin/" not in req.path and req.path != "/api/signup/" and req.path not in "/api/token/" and req.path != "/api/loginrequest/" and req.path != "/api/loginverified/" and req.path != "/api/resendotp/" and req.path != "/api/adminLogin/" and req.path != "/api/adminSignup/" and req.path != "/api/addSlab/" and req.path != "/api/callDailyLedger/":
            try:
                merchant_id = req.headers["auth_token"]
                merchant_id = auth.AESCipher(
                    const.AuthKey, const.AuthIV).decrypt(merchant_id)

                bomodel = BO_User_Service.fetch_by_id(int(merchant_id))
                if bomodel == None:
                    print('enter if')
                    error_res = HttpResponse(
                        str({"message": "user not valid"}))
                    error_res['Content-Type'] = 'application/json'
                    return error_res

            except Exception as e:
                import traceback
                print(traceback.format_exc())
                error_res = HttpResponse(str({"message": e.args}))
                error_res['Content-Type'] = 'application/json'
                return error_res
        res = get_response(req)
        return res
    return middleware
