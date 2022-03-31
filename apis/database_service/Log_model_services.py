from logging import log
from ..models import LogModel
from datetime import datetime
import math
class Log_Model_Service:
    def __init__(self,log_type=None,client_ip_address=None,json={},table_id=None,table_name=None,server_ip_address=None,remarks=None,full_request=None,created_by=None):
        
        self.log_type=log_type
        self.client_ip_address=client_ip_address
        self.server_ip_address=server_ip_address
        self.table_id = table_id
        self.table_name=table_name
        self.remarks = remarks
        self.full_request = full_request
        self.json=json
        # self.full_response = full_response
        self.created_by=created_by
    def save(self)->int:
        logmodel = LogModel()
        logmodel.table_name=self.table_name
        logmodel.table_primary_id=self.table_id
        logmodel.log_type=self.log_type
        logmodel.client_ip_address=self.client_ip_address
        logmodel.server_ip_address=self.server_ip_address
        logmodel.remarks=self.remarks
        logmodel.full_request=self.full_request
        logmodel.json=self.json
        # logmodel.full_response=self.full_response
        logmodel.created_by=self.created_by
        logmodel.save()
        return logmodel.id
    @staticmethod
    def fetch_by_id(id)->LogModel:
        logmodel = LogModel.objects.get(id=id)
        return logmodel
    @staticmethod
    def update_response(id,response)->LogModel:
        logmodel = LogModel.objects.get(id=id)
        logmodel.full_response = response
        logmodel.updated_at=datetime.now()
        logmodel.save()
        return logmodel
    @staticmethod
    def fetch_all_logs_in_parts(page,length,start,end)->list:
        page=int(page)
        length=int(length)
        if start=="all" or end=="all":
            print("select * from apis_logmodel  order by id desc  limit "+str(length)+" offset "+str((page-1)*length)+"")
            logmodel=LogModel.objects.raw("select * from apis_logmodel  order by id desc  limit "+str(length)+" offset "+str((page-1)*length)+"")
            
        else:
            # logmodel=LogModel.objects.filter(created_at__range=[start,end])
            print("select * from apis_logmodel order by id desc between '"+str(start)+"' and '"+str(end)+"' limit "+str(length)+" offset "+str((page-1)*length)+"")
            logmodel=LogModel.objects.raw("select * from apis_logmodel order by id desc between '"+str(start)+"' and '"+str(end)+"' limit "+str(length)+" offset "+str((page-1)*length)+"")
            

            
        def rec(rec1):
                json = {"id":rec1.id,"log_type":rec1.log_type,"client_ip_address":rec1.client_ip_address,"server_ip_address":rec1.server_ip_address,"table_primary_id":rec1.table_primary_id,"table_name":rec1.table_name,"remarks":rec1.remarks,"full_request":rec1.full_request,"full_response":rec1.full_response,"created_at":rec1.created_at,"deleted_at":rec1.deleted_at,"updated_at":rec1.updated_at,"created_by":rec1.created_by,"updated_by":rec1.updated_by,"deleted_by":rec1.deleted_by}
                return json
        # print(list(logmodel.iterator()))
        logmodel=list(map(rec,list(logmodel.iterator())))
        
        
        # if length=="all":
        #     return logmodel
        # if len(logmodel)==0:
        #     return logmodel
        # length=int(length)
        # splitlen = math.ceil(len(logmodel)/length)
        # split_list = []
        # for i in range(splitlen):
        #     split_list.append(logmodel[length*i:length*(i+1)])
        # split_list.reverse()
        # print(split_list,splitlen)
        return [logmodel,len(logmodel)]


