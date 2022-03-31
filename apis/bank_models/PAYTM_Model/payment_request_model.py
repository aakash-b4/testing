import datetime

class Payment_Request_Model:
    def __init__(self,subwalletGuid=None,beneficiaryName=None,beneficiaryVPA=None,orderId=None,beneficiaryAccount=None,beneficiaryIFSC=None,amount=None,purpose=None,transfer_mode=None):
        self.subwalletGuid=subwalletGuid
        self.orderId=orderId
        self.beneficiaryVPA=beneficiaryVPA
        self.beneficiaryName=beneficiaryName
        self.beneficiaryAccount=beneficiaryAccount
        self.beneficiaryIFSC=beneficiaryIFSC
        self.amount=amount
        self.purpose=purpose
        self.transfer_Mode = transfer_mode
        # self.date=date
    def to_json(self):
        if self.transfer_Mode=="RTGS" or self.transfer_Mode=="NEFT":
             return {
            "subwalletGuid":self.subwalletGuid,
            "orderId":self.orderId,
            "beneficiaryName":self.beneficiaryName,
            "beneficiaryAccount":self.beneficiaryAccount,
            "beneficiaryIFSC":self.beneficiaryIFSC,
            "amount":self.amount,
            "transferMode":self.transfer_Mode,
            "purpose":self.purpose,
            "comments": "disbursal",
            "date":str(datetime.date.today())
        }
        elif self.transfer_Mode=="UPI":
             return {
            "subwalletGuid":self.subwalletGuid,
            "orderId":self.orderId,
            "beneficiaryVPA":self.beneficiaryVPA,
            "amount":self.amount,
            "transferMode":self.transfer_Mode,
            "purpose":self.purpose,
            "comments": "disbursal",
            "date":str(datetime.date.today())
        }
        else:
            return {
                "subwalletGuid":self.subwalletGuid,
                "orderId":self.orderId,
                "beneficiaryAccount":self.beneficiaryAccount,
                "beneficiaryIFSC":self.beneficiaryIFSC,
                "amount":self.amount,
                "transferMode":self.transfer_Mode,
                "purpose":self.purpose,
                "comments": "disbursal",
                "date":str(datetime.date.today())
            }




