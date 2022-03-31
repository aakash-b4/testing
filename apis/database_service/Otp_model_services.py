from ..database_models.OtpModel import OtpModel
from datetime import datetime,timedelta,timezone
import pytz
class Otp_Model_Services:
    def __init__(self,user_id=None,user_type=None,type=None,verification_token=None,mobile=None,email=None,otp=None,expire_datetime=None,otp_status=None):
        self.user_id = user_id
        self.user_type=user_type
        self.verification_token=verification_token
        self.mobile=mobile
        self.type=type
        self.email=email
        self.otp=otp
        self.expire_datetime=expire_datetime
        self.otp_status=otp_status
    def save(self)->int:
        otp_model = OtpModel()
        otp_model.user_id=self.user_id
        otp_model.type=self.type
        otp_model.user_type=self.user_type
        otp_model.verification_token=self.verification_token
        otp_model.mobile=self.mobile
        otp_model.email=self.email
        otp_model.otp=self.otp
        time_add= timedelta(minutes=5)
        otp_model.expire_datetime=datetime.now()+time_add
        otp_model.otp_status=self.otp_status
        otp_model.save()
        return otp_model.id
    @staticmethod
    def fetch_by_verification_token_with_otp(verification_token,otp,type):
        otp_model = OtpModel.objects.filter(verification_token=verification_token,otp_status="pending",otp=otp,type=type)
        dt=datetime.now(pytz.timezone('Asia/Kolkata'))
        print("time")

        
        print(otp_model)
        if(len(otp_model)>0 and otp_model[0].expire_datetime<dt):
            print("if")
            Otp_Model_Services.update_status(otp_model[0].id,"Expired")
            return ["OTP Expired"]
        return otp_model
    @staticmethod
    def fetch_by_verification_only(verification_token):
        print("excuting")
        otp_model = OtpModel.objects.filter(verification_token=verification_token,otp_status__in=["pending","Expired"])
        if(len(otp_model)>0):
         return otp_model[0]
        else:
            return None
    @staticmethod
    def update_status(id,status):
        otp_model = OtpModel.objects.filter(id=id,otp_status="pending")
        print(otp_model)
        if len(otp_model)>0:
         otp_model=otp_model[0]
         otp_model.otp_status=status
         otp_model.updated_at=datetime.now()
         otp_model.save()
        return True
    
