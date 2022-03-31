from apis.database_models import LedgerModel
import random
from datetime import datetime
import uuid

def generate_token():
    payout_txnid=str(datetime.now()).replace("-","")+str(random.randint(10,50))
    payout_txnid=payout_txnid.replace(" ","").replace(":","").replace(".","")
    return payout_txnid

def generate_unique_customerRef():
    resp = "CR"+str(uuid.uuid1()).split("-")[0]+generate_token()
    return resp