class Header_Response:
    def __init__(self,rslt=None,error=None):
        self.rslt=rslt
        self.error=error
        
    def from_json(self,json):
        self.rslt=json["rslt"]
        self.error=json["error"]
        


class Body_Response:
    def __init__(self,custRef=None,coreRef=None,instNo=None,cmsRef=None,status=None,statusDesc=None,errorCode=None,clientCode=None,dateTime=None,impsStatus=None,impsStatusDesc=None,impsBeneAccDest=None,impsBeneNameDest=None):
        self.custRef=custRef
        self.coreRef=coreRef
        self.instNo=instNo
        self.cmsRef=cmsRef
        self.status=status
        self.statusDesc=statusDesc
        self.errorCode=errorCode
        self.clientCode=clientCode
        self.dateTime=dateTime
        self.impsStatus=impsStatus
        self.impsStatusDesc=impsStatusDesc
        self.impsBeneAccDest=impsBeneAccDest
        self.impsBeneNameDest=impsBeneNameDest
    def from_json(self,json={}):
        try:
            self.custRef=json["custRef"]
            self.coreRef=json["coreRef"]
            self.instNo=json["instNo"]
            self.cmsRef=json["cmsRef"]
            self.status=json["status"]
            self.statusDesc=json["statusDesc"]
            self.errorCode=json["errorCode"]
            self.clientCode=json["clientCode"]
            self.dateTime=json["dateTime"]
            self.impsStatus=json["impsStatus"]
            self.impsStatusDesc=json["impsStatusDesc"]
            self.impsBeneAccDest=json["impsBeneAccDest"]
            self.impsBeneNameDest=json["impsBeneNameDest"]
        
            return True
        except Exception as e:
            print("Exception : "+ e.args)
            return False






