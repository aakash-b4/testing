class Payment_Response_Model:
    def __init__(self,status=None,statusCode=None,statusMessage=None):
        self.status = status
        self.statusCode=statusCode
        self.statusMessage=statusMessage

    @staticmethod
    def from_json(json={}):
        payment_response_model=Payment_Response_Model()
        payment_response_model.status=json["status"]
        payment_response_model.statusCode=json['statusCode']
        payment_response_model.statusMessage=json['statusMessage']
        return payment_response_model
