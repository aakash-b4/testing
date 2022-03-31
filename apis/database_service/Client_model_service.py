from apis.database_models.BOUserModel import BOUserModel
from ..models import MerchantModel as ClientModel
from . import Log_model_services
from .. import const
from django.db import connection
from sabpaisa import auth
from ..const import *


class Client_Model_Service:
    def __init__(self, email=None, client_id=None, client_name=None, is_charge=None, phone_number=None, client_code=None, role_id=None, auth_key=None, user=None, auth_iv=None, bank_id=None, client_username=None, client_password=None):
        self.client_id = client_id
        self.client_code = client_code
        self.auth_key = auth_key
        self.user = user
        self.auth_iv = auth_iv
        self.bank_id = bank_id
        self.client_username = client_username
        self.role_id = role_id
        self.client_name = client_name
        self.phone_number = phone_number
        # self.is_charge=is_charge
        self.client_password = client_password
        self.email = email

    def save(self, client_ip_address, created_by) -> int:
        log_service = Log_model_services.Log_Model_Service(log_type="create", table_name="apis_clientmodel", remarks="saving records in apis_clientmodel table",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)

        clientmodel = ClientModel()
        clientmodel.client_name = self.client_name
        clientmodel.client_id = self.client_id
        clientmodel.client_code = self.client_code
        clientmodel.auth_key = self.auth_key
        clientmodel.role_id = self.role_id
        clientmodel.auth_iv = self.auth_iv
        clientmodel.bank_id = self.bank_id
        clientmodel.encrypted_password = str(auth.AESCipher(
            const.AuthKey, const.AuthIV).encrypt(self.client_password))[2:].replace("'", "")
        clientmodel.phone = self.phone_number
        clientmodel.client_username = self.client_username
        clientmodel.client_password = self.client_password
        clientmodel.user_id = self.user
        clientmodel.email = self.email
        # clientmodel.is_charge=self.is_charge
        clientmodel.save()
        log_service.table_id = clientmodel.id
        log_service.save()
        return clientmodel.id

    # @staticmethod
    # def fetch_by_id_filter(id,client_ip_address,created_by)->ClientModel:
    #     log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_clientmodel",remarks="fetching records in apis_clientmodel table by primary key id",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)

    #     clientModel=ClientModel.objects.filter(id=id,status=True)
    #     model=clientModel
    #     return model
    @staticmethod
    def fetch_by_id(id, client_ip_address, created_by) -> ClientModel:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching records in apis_clientmodel table by primary key id",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        try:
            clientModel = ClientModel.objects.get(id=id, status=True)
            print(clientModel, "client_model")
            model = clientModel
            if clientModel:
                log_service.table_id = model.id
            log_service.save()
            return model
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def fetch_by_clientid(client_id, client_ip_address, created_by) -> ClientModel:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching records in apis_clientmodel table by client id",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)

        clientModels = ClientModel.objects.filter(
            client=client_id, status=True)
        model = clientModels[0]
        log_service.table_id = model.id
        log_service.save()
        return model

    @staticmethod
    def fetch_by_clientcode(client_code, client_ip_address, created_by) -> ClientModel:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching records in apis_clientmodel table by client code",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)

        clientModel = ClientModel.objects.filter(
            client_code=client_code, status=True)
        model = clientModel[0]
        return model

    @staticmethod
    def fetch_all_by_clientcode(client_code, client_ip_address, created_by) -> list:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching all records in apis_clientmodel table by client code",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        log_service.save()
        clientModel = ClientModel.objects.filter(
            client_code=client_code, status=True)
        return clientModel

    def fetchAuth(client_code, created_by) -> ClientModel:
        # log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching records in apis_clientmodel table by client code",
        #                                                    client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        clientModel = ClientModel.objects.filter(
            client_code=client_code, status=True)
        model = clientModel[0]

        return model

    @staticmethod
    def fetch_by_email(email, client_ip_address, created_by) -> list:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching all records in apis_clientmodel table by email",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        log_service.save()
        clientModel = ClientModel.objects.filter(email=email, status=True)
        print(clientModel)
        return clientModel

    @staticmethod
    def fetch_by_username_password(username, password, client_ip_address, created_by) -> list:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching all records in apis_clientmodel table by username",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        log_service.save()
        clientModel = ClientModel.objects.filter(
            client_username=username, client_password=password, status=True)
        return clientModel

    @staticmethod
    def fetch_by_username_encrypted_password(username, password, client_ip_address, created_by) -> list:
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_clientmodel", remarks="fetching all records in apis_clientmodel table by username",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        log_service.save()
        clientModel = ClientModel.objects.filter(
            client_username=username, encrypted_password=password, status=True)
        return clientModel

    @staticmethod
    def get_user_type(merchant_id) -> list:
        cursors = connection.cursor()
        cursors.execute('call getRoleType("'+str(merchant_id)+'")')
        # cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        # print(value)
        return value
        # log_service.save()

    @staticmethod
    def get_all_merchants(page, length):
        offSet = (int(page)-1)*int(length)
        query = "call fetchMerchants("+str(length)+","+str(offSet)+");"
        resp = list()
        record = ClientModel.objects.raw(query)
        print(record.columns)
        for b in list(record.iterator()):
            d = {
                'id': b.id,
                "client_name": b.client_name,

                'role': b.role_id,
                'client': b.client_id,
                'client_code': b.client_code,
                'auth_key': b.auth_key,
                'auth_iv': b.auth_iv,
                'bank': b.bank_id,
                'client_username': b.client_username,
                'encrypted_client_password': b.encrypted_password,
                'is_payout': b.is_payout,
                'is_merchant': b.is_merchant,
                'status': b.status,
                'created_at': b.created_at,
                'deleted_at': b.deleted_at,
                'updated_at': b.updated_at,
                'user': b.user_id,
                'created_by': b.created_by,
                'updated_by': b.updated_by,
                'deleted_by': b.deleted_by,
                'is_ip_checking': b.is_ip_checking,
                'email': b.email,
                'phone': b.phone,
                'is_charge': b.is_charge,
                'is_ip_checking': b.is_ip_checking,
                'is_encrypt': b.is_encrypt

            }
            resp.append(d)
        result = list(map(enc, resp))
        return result


def enc(b):
    encId = str(auth.AESCipher(const.AuthKey,
                const.AuthIV).encrypt(str(b["id"])))
    d = {
        'auth token': encId[2:].replace("'", ""),
        "id": b["id"],
        "client_name": b["client_name"],
        'role': b.get("role"),
                'client': b.get("client"),
                'client_code': b.get("client_code"),
                'auth_key': b.get("auth_key"),
                'auth_iv': b.get("auth_iv"),
                'bank': b.get("bank"),
                'client_username': b.get("client_username"),
                'encrypted_client_password': b.get("encrypted_client_password"),
                'is_payout': b.get("is_payout"),
                'is_merchant': b.get("is_merchant"),
                'status': b.get("status"),
                'created_at': b.get("created_at"),
                'deleted_at': b.get("deleted_at"),
                'updated_at': b.get("updated_at"),
                'user': b.get("user"),
                'created_by': b.get("created_by"),
                'updated_by': b.get("updated_by"),
                'deleted_by': b.get("deleted_by"),
                'is_ip_checking': b.get("is_ip_checking"),
                'email': b.get("email"),
                'phone': b.get("phone"),
                'is_charge': b.get("is_charge"),
                'is_ip_checking': b.get("is_ip_checking"),
                'is_encrypt': b.get("is_encrypt"),
    }
    return d
