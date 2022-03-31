from datetime import datetime
from math import trunc

from rest_framework import status
from ..database_models.RoleModel import RoleModel
from ..database_service.Log_model_services import Log_Model_Service
from ..const import server_ip

class Role_Model_service:
    def __init__(self,role_name=None,permited_apis=None):
        self.role_name=role_name
        self.permited_apis=permited_apis
    def save(self,admin_id,client_ip_address):
        log = Log_Model_Service(log_type="save",client_ip_address=client_ip_address,table_name="apis_rolemodel",server_ip_address=server_ip,
    remarks="saving role record by admin id :: "+str(admin_id))
        roleModel = RoleModel()
        roleModel.role_name=self.role_name
        roleModel.permited_apis = self.permited_apis
        roleModel.created_by="admin ID :: "+str(admin_id)
        resp = RoleModel.objects.filter(role_name=self.role_name,permited_apis=self.permited_apis,status=True)
        if(len(resp)!=0):
            return 0
        roleModel.save()
        log.table_id=roleModel.id
        log.save()
    @staticmethod
    def fetchRoles(admin_id,client_ip_address):
        log = Log_Model_Service(log_type="save",client_ip_address=client_ip_address,table_name="apis_rolemodel",server_ip_address=server_ip,
        remarks="saving role record by admin id :: "+str(admin_id))
        roleModel = RoleModel.objects.filter(status=True).values()
        if(len(roleModel)==0):
            return 0
        resp = list()
        for role in roleModel:
            d={
                "role_name":role.get("role_name"),
                "permited_apis":role.get("permited_apis")
            }
            resp.append(d)
        log.save()
        return resp
    @staticmethod
    def deleteRole(role_name,admin_id,client_ip_address):
        log = Log_Model_Service(log_type="save",client_ip_address=client_ip_address,table_name="apis_rolemodel",server_ip_address=server_ip,
        remarks="delete role record by admin id :: "+str(admin_id))
        roleModel = RoleModel.objects.filter(role_name=role_name,status=True)
        if(len(roleModel)==0):
            return 0
        roleModel[0].status=False
        roleModel[0].deleted_by="admin ID :: "+str(admin_id)
        roleModel[0].deleted_at=datetime.now()
        roleModel[0].save()
        # roleModel[0].get("status")=False
        # roleModel[0].get("deleted_by")="admin ID :: "+str(admin_id)
        # roleModel[0].get("deleted_by")=datetime.now()
        # roleModel[0].save()
        # print(roleModel[0].get("status"))
        log.save()
        return 1