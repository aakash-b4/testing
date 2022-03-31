from apis.database_models.CIBRegistrationModel import CIBRegistration

class CIBRegistrationResponse:
    def __init__(self, status, Message, ErrorCode, success, Response):
        self.status = status
        self.Message = Message
        self.ErrorCode = ErrorCode
        self.success = success
        self.Response = Response


    def to_json(self):
        return {
            "status": self.status,
            "Message": self.Message,
            "ErrorCode": self.ErrorCode,
            "success": self.success,
            "Response": self.Response
        }

    @staticmethod
    def from_json(json_object):
        return CIBRegistrationResponse(
            status=json_object.get("status", ""),
            Message=json_object.get("Message", ""),
            ErrorCode=json_object.get("ErrorCode", ""),
            success=json_object.get("success", ""),
            Response=json_object.get("Response", "")
        )

    # function to convert CIBRegistrationResponseModel object to CIBRegistration object
    @staticmethod
    def to_CIBRegistration(CIBRegistrationResponseModel_object):
        return CIBRegistration(
            aggrName=CIBRegistrationResponseModel_object.Response.get("AGGRNAME"),
            aggrId=CIBRegistrationResponseModel_object.Response.get("AGGRID"),
            corpId=CIBRegistrationResponseModel_object.Response.get("CORPID"),
            userId=CIBRegistrationResponseModel_object.Response.get("USERID"),
            urn=CIBRegistrationResponseModel_object.Response.get("URN"),
            aliasId=CIBRegistrationResponseModel_object.Response.get("ALIASID")
        )

