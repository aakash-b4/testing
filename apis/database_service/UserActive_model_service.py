from django.utils.translation import activate
from ..database_models.UserActiveModel import UserActiveModel
from datetime import date, datetime,timedelta,timezone
from ..Utils import randomstring
class UserActive_Model_Service:
    def __init__(self,merchant_id=None,active_status=None,login_status=None,client_ip_address=None,last_server_call_time=None,geo_location=None,login_time=None,login_expire_time=None):
        self.merchant_id=merchant_id
        self.active_status=active_status
        self.login_status=login_status
        self.client_ip_address=client_ip_address
        self.last_server_call_time=last_server_call_time
        self.geo_location=geo_location
        self.login_time=login_time
        # self.login_expire_time=login_expire_time
    def save(self):
        useractivemodel = UserActiveModel()
        useractivemodel.merchant_id=self.merchant_id
        useractivemodel.active_status=self.active_status
        useractivemodel.login_status=self.login_status
        useractivemodel.client_ip_address=self.client_ip_address
        # useractivemodel.last_server_call_time=self.last_server_call_time
        useractivemodel.geo_location=self.geo_location
        useractivemodel.login_time=self.login_time
        login_expire_add=timedelta(days=3)
        useractivemodel.login_expire_time=datetime.now()+login_expire_add
        tab_time_add= timedelta(hours=1)
        useractivemodel.tab_token_expire_time=datetime.now()+tab_time_add
        useractivemodel.login_token=randomstring.randomString(length=30)
        useractivemodel.tab_token=randomstring.randomString(length=30)
        useractivemodel.save()
        return {"id":useractivemodel.id,"tab_token":useractivemodel.tab_token,"login_token":useractivemodel.login_token}
    @staticmethod
    def fetch_by_id(id):
        active = UserActiveModel.objects.get(id=id)
        return active
    @staticmethod
    def fetch_by_merchant_id(merchant_id)->UserActiveModel:
        active = UserActiveModel.objects.filter(merchant_id=merchant_id)
        if len(active)==0:
            return None
        return active[0]
    @staticmethod 
    def update_login_exipre(id,time):
        active = UserActiveModel.objects.get(id=id)
        active.login_expire_time=time
        active.save()
        return active.id
    @staticmethod 
    def update_tab_exipre(id,time):
        active = UserActiveModel.objects.get(id=id)
        active.tab_token_expire_time=time
        active.save()
        return active.id
    @staticmethod 
    def update_active_status(id,status):
        active = UserActiveModel.objects.get(id=id)
        active.active_status=status
        active.save()
        return active.id
    @staticmethod 
    def recreate_tab_token(id):
        active = UserActiveModel.objects.get(id=id)
        active.active_status="active"
        active.tab_token_expire_time=datetime.now()+timedelta(hours=1)
        active.tab_token=randomstring.randomString(length=30)
        active.save()
        return {"id":active.id,"tab_token":active.tab_token}
    @staticmethod
    def check_active_user(login_token,tab_token):
        active = UserActiveModel.objects.filter(login_status="active",login_expire_time__gt=datetime.now(),tab_token_expire_time__gt=datetime.now()).exclude(login_token=login_token,tab_token=tab_token)
        
        return active




