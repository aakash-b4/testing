from ..database_models.WebhookRequestModel import WebhookRequestModel

from datetime import datetime

class Webhook_Request_Model_Service:
    def __init__(self,payout_trans_id=None,hit_init_time=None,status=None):
        self.payout_trans_id=payout_trans_id
        self.hit_init_time=hit_init_time
        self.status=status
       
    def save(self)->int:
        webhookrequestmodel=WebhookRequestModel()
        webhookrequestmodel.payout_trans_id=self.payout_trans_id
        webhookrequestmodel.hit_init_time=self.hit_init_time
        webhookrequestmodel.status=self.status
        webhookrequestmodel.created_on=datetime.now()
        
        webhookrequestmodel.save()
        return webhookrequestmodel.id
    @staticmethod
    def update_webhook(id,status,merchant_response):
        try:
            webhookrequestmodel=WebhookRequestModel.objects.get(id=id)
            webhookrequestmodel.trans_complete_time=datetime.now()
            webhookrequestmodel.response_from_merchant=merchant_response
            webhookrequestmodel.updated_on=datetime.now()
            webhookrequestmodel.status=status
            webhookrequestmodel.save()
            return True
        except Exception as e:
            return False


        
