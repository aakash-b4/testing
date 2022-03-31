# from ..database_models.OtpModel import OtpModel
from ..database_models.SlabModel import SlabModel
from datetime import date, datetime,timedelta,timezone

class Slab_Model_Service:
    def __init__(self,merchant_id=None,min_amount=None,max_amount=None):
        self.merchant_id=merchant_id
        self.min_amount=min_amount
        self.max_amount=max_amount
    def save(self)->int:
        # slabmodel = SlabModel.objects.filter(merchant_id=self.merchant_id)
        # if len(slabmodel)!=0:
        #     return None
        slabmodel = SlabModel()
        slabmodel.merchant_id=self.merchant_id
        slabmodel.min_amount=self.min_amount
        slabmodel.max_amount=self.max_amount
        slabmodel.save()
        return slabmodel.id
    def fetch_by_id(id=None):
        slabmodel=SlabModel.objects.get(id=id)
        return slabmodel
    def check_slab(merchant_id,amount):
        slabmodel=SlabModel.objects.filter(merchant_id=merchant_id,max_amount__gte=amount,min_amount__lte=amount)
        if len(slabmodel)==0:
            return False
        return True
    def fetch_by_merchant_id(merchant_id):
        slabmodel=SlabModel.objects.filter(merchant_id=merchant_id,status=True)
        return slabmodel
    def delete_slab(id):
        slabmodel=SlabModel.objects.get(id=id)
        slabmodel.deleted_at=datetime.now()
        slabmodel.status=False
        slabmodel.save()
        return slabmodel
    def update_slab(slabmodelup):
        slabmodel=SlabModel.objects.get(id=slabmodelup.id)
        slabmodel.status=False
        slabmodel.deleted_at=datetime.now()
        
        slabmodel.save()
        slabmodelup.created_at=datetime.now()
        slabmodelup.updated_at=datetime.now()
        slabmodelup.save()
        return slabmodel

