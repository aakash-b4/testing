from datetime import datetime
from ..database_models import ChargeBreakingModel

from . import Log_model_services
from .. import const
from sabpaisa import auth

class Charge_Breaking_model_services:
    def __init__(self,charge_amount=None,charge_id=None,charge_type=None,transaction_id=None,payout_transaction_id=None,tax_amount=None):
        self.charge_amount=charge_amount
        self.charge_id=charge_id
        self.transaction_id=transaction_id
        self.charge_type=charge_type
        self.payout_transaction_id=payout_transaction_id
        self.tax_amount=tax_amount
    def save(self):
        chargebreakingmodel=ChargeBreakingModel.ChargeBreakingModel()
        chargebreakingmodel.charge_amount=self.charge_amount
        chargebreakingmodel.charge_type=self.charge_type
        chargebreakingmodel.charge_id=self.charge_id
        chargebreakingmodel.transaction_id=self.transaction_id
        chargebreakingmodel.payout_transaction_id=self.payout_transaction_id
        chargebreakingmodel.tax_amount=self.tax_amount
        chargebreakingmodel.created_on=datetime.now()
        chargebreakingmodel.created_by="system"
        chargebreakingmodel.save()
        return chargebreakingmodel
        