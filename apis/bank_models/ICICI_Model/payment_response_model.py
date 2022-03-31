class Response_Model:
    def __init__(self,status=None,customerReferenceNumber=None,bankReferenceNumber=None,TransRefNo=None,BeneName=None,errorDetails=None,errorCode=None,errorDescription=None,errorType=None,errorSource=None,timestamp=None):
        self.status=status
        self.customerReferenceNumber=customerReferenceNumber
        self.bankReferenceNumber=bankReferenceNumber
        self.TransRefNo=TransRefNo
        self.BeneName=BeneName
        self.errorDetails=errorDetails
        self.errorCode=errorCode
        self.errorDescription=errorDescription
        self.errorType=errorType
        self.errorSource=errorSource
        self.timestamp=timestamp 
    @staticmethod
    def from_json(json={}):
        response_model=Response_Model()
        response_model.status=json["status"]
        response_model.customerReferenceNumber=json["customerReferenceNumber"]
        response_model.bankReferenceNumber=json["bankReferenceNumber"]
        response_model.BeneName=json["BeneName"]
        response_model.errorDetails=json["errorDetails"]
        response_model.errorCode=json["errorCode"]
        response_model.errorDescription=json["errorDescription"]
        response_model.errorType=json["errorType"]
        response_model.errorSource=json["errorSource"]
        response_model.timestamp=json["timestamp"]
        response_model.TransRefNo=json['TransRefNo']
        return response_model

