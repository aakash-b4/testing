from ..models import BOUserModel

from . import Log_model_services
from .. import const
from sabpaisa import auth
class BO_User_Service:
    def __init__(self,roleid=None,username=None,user_id=None,password=None,name=None,auth_key=None,auth_iv=None,email=None,mobile=None):
        self.roleid=roleid
        self.username=username
        self.password=password
        self.name=name
        self.email=email
        self.auth_key=auth_key
        self.auth_iv=auth_iv
        self.mobile=mobile
        self.user_id=user_id
    def save(self,client_ip_address,created_by):
        bouser = BOUserModel()
        bouser.role_id=self.roleid
        bouser.username=self.username
        bouser.password=self.password
        bouser.name=self.name
        bouser.email=self.email
        bouser.django_user_id=self.user_id
        bouser.auth_key=self.auth_key
        bouser.auth_iv=self.auth_iv
        bouser.mobile=self.mobile
        bouser.encrypted_password=str(auth.AESCipher(const.AuthKey,const.AuthIV).encrypt(self.password))[2:].replace("'","")
        bouser.save()
        return bouser.id
    @staticmethod
    def fetch_by_name(name,client_ip_address,created_by):
        bouser=BOUserModel.objects.filter(name=name,status=True)
        
        return bouser
    @staticmethod
    def fetch_by_name(email,client_ip_address,created_by):
        bouser=BOUserModel.objects.filter(email=email,status=True)
        
        return bouser
    @staticmethod
    def fetch_by_username_password(username,password,client_ip_address,created_by):
        bouser = BOUserModel.objects.filter(username=username,password=password,status=True)
        
        return bouser
    @staticmethod
    def fetch_by_username_encrypted_password(username,password,client_ip_address,created_by):
        bouser = BOUserModel.objects.filter(username=username,encrypted_password=password,status=True)
        
        return bouser
    @staticmethod
    def fetch_user_type(id):
        bouser = BOUserModel.objects.get(id=id,status=True)
        if bouser == None:
            return None
        return bouser.role_id
    @staticmethod
    def fetch_by_id(id)->BOUserModel:
        try:
         bouser = BOUserModel.objects.get(id=id,status=True)
         return bouser
        except Exception as e:
            return None

    @staticmethod
    def fetch_by_email(email)->BOUserModel:
        
         bouser = BOUserModel.objects.filter(email=email,status=True)
         return bouser
        
    

    
        