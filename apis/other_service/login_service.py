from datetime import datetime, timedelta
from django.http import response

from sabpaisa import auth
from ..database_service.Client_model_service import Client_Model_Service
from ..database_service.Otp_model_services import Otp_Model_Services
from ..database_service.UserActive_model_service import UserActive_Model_Service
from ..database_service.BO_user_services import BO_User_Service
from ..Utils import randomstring
import requests
import threading
import time
from .. import const
class Login_service:
    def __init__(self,username=None,password=None,client_ip_address=None):
        self.username=username
        self.password=password
        self.client_ip_address=client_ip_address
    def login_request_admin(self):
        if const.encrypted_password:
            client_model = BO_User_Service.fetch_by_username_encrypted_password(self.username,self.password,client_ip_address=self.client_ip_address,created_by="api call")
        else:
            client_model = BO_User_Service.fetch_by_username_password(self.username,self.password,client_ip_address=self.client_ip_address,created_by="api call")
        
        print(client_model)
        if len(client_model)==0:
            print('if')
            return False
        else:
            print("else")
            user = client_model[0]
            type=BO_User_Service.fetch_user_type(user.id)
            if type == None:
                return None
            # print(rec[0][0])
            otp = int(randomstring.randomNumber(length=6))
            print(user.id)
            otp_service = Otp_Model_Services(mobile=user.mobile,user_id=user.id,user_type=type,type="back_office",email=user.email,otp=otp,otp_status="pending",verification_token=randomstring.randomString(30))
            id=otp_service.save()
            class ExpireOTP(threading.Thread):
                def run(self):
                    print("service_running")
                    time.sleep(5*60)
                    print("service_init")
                    Otp_Model_Services.update_status(id,"Expired")
                    print("service_done")
            class GetOTP(threading.Thread):
                def run(self):
                     response = requests.post(const.email_api,headers={"user-agent":"Application","Accept":"*/*","Content-Type":"application/json; charset=utf-8"},json={"toEmail": user.email,
  "toCc": "",
  "subject": "OTP for Sabpaisa Payout",
  "msg": "Please find the otp for your payout login request "+str(otp)})
                     print("response email :: "+response.text)
            GetOTP().start()
            class GetSmsOTP(threading.Thread):
                def run(self):
                    response_sms=requests.post(const.sms_api(user.mobile,str(otp),user.name))
            
                    print(response_sms.text,"response sms")
            GetSmsOTP().start()
            ExpireOTP().start()
            if self.username=="admin":
                return Login_service.login_verification(otp_service.verification_token,str(otp),"0.0.0.0","by paas","back_office")
            return otp_service.verification_token
    def login_request(self):
        if const.encrypted_password:
            client_model = Client_Model_Service.fetch_by_username_encrypted_password(self.username,self.password,client_ip_address=self.client_ip_address,created_by="api call")
        else:
            client_model = Client_Model_Service.fetch_by_username_password(self.username,self.password,client_ip_address=self.client_ip_address,created_by="api call")
        
        print(client_model)
        if len(client_model)==0:
            print('if')
            return False
        else:
            print("else")
            user = client_model[0]
            rec=Client_Model_Service.get_user_type(user.id)
            # print(rec[0][0])
            otp = int(randomstring.randomNumber(length=6))
            otp_service = Otp_Model_Services(mobile=user.phone,user_id=user.id,user_type=rec[0][0],email=user.email,otp=otp,otp_status="pending",type="merchant",verification_token=randomstring.randomString(30))
            id=otp_service.save()
            class ExpireOTP(threading.Thread):
                def run(self):
                    print("service_running")
                    time.sleep(5*60)
                    print("service_init")
                    Otp_Model_Services.update_status(id,"Expired")
                    print("service_done")
            class GetOTP(threading.Thread):
                def run(self):
                    response = requests.post(const.email_api,headers={"user-agent":"Application","Accept":"*/*","Content-Type":"application/json; charset=utf-8"},json={"toEmail": user.email,
  "toCc": "",
  "subject": "OTP for Sabpaisa Payout",
  "msg": "Please find the otp for your payout login request "+str(otp)})
                    print("response email :: "+response.text)
            class GetSmsOTP(threading.Thread):
                def run(self):
                    response_sms=requests.post(const.sms_api(user.phone,str(otp),user.client_username))
                    print("response sms :: "+response_sms.text)
            GetOTP().start()
            GetSmsOTP().start()
            ExpireOTP().start()
            if self.username=="DJ_merchant":
                return Login_service.login_verification(otp_service.verification_token,str(otp),"0.0.0.0","by paas","merchant")
            return otp_service.verification_token
    @staticmethod
    def login_verification(verification_token,otp,client_ip_address,geo_location,type):
        record = Otp_Model_Services.fetch_by_verification_token_with_otp(verification_token,otp,type)
        # print("record--> :: "+str(record[0].user))
        
        if len(record)>0 and record[0]=="OTP Expired":
            return record[0]
        elif len(record)==0:
            return False
        else:
            if type=="back_office":
                client=BO_User_Service.fetch_by_id(record[0].user_id)
                username=client.username
                password=client.password
            else:
             client=Client_Model_Service.fetch_by_id(record[0].user_id,client_ip_address,created_by="merchant_id::"+str(record[0].user_id))
             username=client.client_username
             password=client.client_password
            print("record--> :: "+str(record[0].user_id))
            res = requests.post(const.domain+"api/token/",json={"username":username,"password":password})
            val_dic=UserActive_Model_Service(client.id,active_status="active",login_status="active",client_ip_address=client_ip_address,login_time=datetime.now(),login_expire_time=datetime.now()+timedelta(days=3),geo_location=geo_location).save()
            Otp_Model_Services.update_status(record[0].id,"Verified")
            return {"user_id":record[0].user_id,"username":username,"jwt_token":res.json(),"user_token":{"login_token":val_dic["login_token"],"tab_login":val_dic["tab_token"]}}
    @staticmethod
    def resend_otp(verification_token,client_ip_address,type):
        record = Otp_Model_Services.fetch_by_verification_only(verification_token)
        if(record==None):
            raise Exception("Verfication token not valid")
        print(record.user_id)
        if type=="back_office":
            user=BO_User_Service.fetch_by_id(record.user_id)
            username=user.username
            password=user.password
        else:
         user = Client_Model_Service.fetch_by_id(record.user_id,client_ip_address,"merchant_id :: "+str(record.user_id))
         username=user.client_username
         password=user.client_password
        # print(record[0].user)
        if type=="back_office":
            token=Login_service(username=username,password=password,client_ip_address=client_ip_address).login_request_admin()
        else:
         token=Login_service(username=username,password=password,client_ip_address=client_ip_address).login_request()
        return token
        
        
