from datetime import datetime
class Message_Header:
    def __init__(self,msgId=None,cnvId=None,extRefId=None,bizObjId=None,appId="CLIENT",timestamp=str(datetime.now())):
        self.msgId=msgId
        self.cnvId=cnvId
        self.extRefId=extRefId
        self.bizObjId=bizObjId
        self.appId=appId
        self.timestamp=timestamp
    def getJson(self):
      
        return { 
                "msgId":str(self.msgId), 
                "cnvId":str(self.cnvId),
                
                "timestamp":self.timestamp 
              } 
class Message_Body:
    def __init__(self,custTxnRef=None,beneAccNo=None,beneName=None,beneAddr1=None,beneAddr2=None,ifsc=None,valueDate=None,tranCcy=None,tranAmount=None,purposeCode=None,remitInfo1=None,remitInfo2=None,clientCode=None,paymentType=None,beneAccType=None,remarks=None,beneMail=None,beneMobile=None):
        self.cusTxnRef=custTxnRef
        self.beneAccNo=beneAccNo
        self.beneName=beneName
        self.beneAddr1=beneAddr1
        self.beneAddr2=beneAddr2
        self.ifsc=ifsc
        self.valueDate=valueDate
        self.tranCcy=tranCcy
        self.tranAmount=tranAmount
        self.purposeCode=purposeCode
        self.remitInfo1=remitInfo1
        self.remitInfo2=remitInfo2
        self.clientCode=clientCode
        self.paymentType=paymentType
        self.beneAccType=beneAccType
        self.remarks=remarks
        self.beneMail=beneMail
        self.beneMobile=beneMobile
    def getJson(self):
        return {
            "msgBdy":{ 
"paymentReq":{ 
"custTxnRef":self.cusTxnRef, 
"beneAccNo":self.beneAccNo, 
"beneName":self.beneName, 
"beneAddr1":self.beneAddr1, 
"beneAddr2":self.beneAddr2, 
"ifsc":self.ifsc, 
"valueDate":self.valueDate, 
"tranCcy":self.tranCcy, 
"tranAmount":self.tranAmount, 
"purposeCode":self.purposeCode, 
"remitInfo1":self.remitInfo1, 
"remitInfo2":self.remitInfo2, 
"clientCode":self.clientCode, 
"paymentType":self.paymentType, 
"beneAccType":self.beneAccType, 
"remarks":self.remarks, 
"beneMail":self.beneMail, 
"beneMobile":self.beneMobile 
} 
}
}


