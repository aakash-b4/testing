from apis.database_models.CIBRegistrationModel import CIBRegistration


class CIBRegistrationRequestModel:
    AGGRNAME = None
    AGGRID = None
    CORPID = None
    USERID = None
    URN = None
    ALIASID = None

    def __init__(self, AGGRNAME="", AGGRID="", CORPID="", USERID="", URN="", ALIASID=""):
        self.AGGRNAME = AGGRNAME
        self.AGGRID = AGGRID
        self.CORPID = CORPID
        self.USERID = USERID
        self.URN = URN
        self.ALIASID = ALIASID

    # function to convert the class object to json
    def to_json(self):
        return {
            "AGGRNAME": self.AGGRNAME,
            "AGGRID": self.AGGRID,
            "CORPID": self.CORPID,
            "USERID": self.USERID,
            "URN": self.URN,
            "ALIASID": self.ALIASID
        }

    # function to convert the json to class object
    @staticmethod
    def from_json(json_object):
        return CIBRegistrationRequestModel(
            AGGRNAME=json_object.get("AGGRNAME", ""),
            AGGRID=json_object.get("AGGRID", ""),
            CORPID=json_object.get("CORPID", ""),
            USERID=json_object.get("USERID", ""),
            URN=json_object.get("URN", ""),
            ALIASID=json_object.get("ALIASID", "")
        )

    # function to convert CIBRegistration object to CIBRegistrationRequestModel object
    @staticmethod
    def from_CIBRegistration(CIBRegistration_object):
        return CIBRegistrationRequestModel(
            AGGRNAME=CIBRegistration_object.aggrName,
            AGGRID=CIBRegistration_object.aggrId,
            CORPID=CIBRegistration_object.corpId,
            USERID=CIBRegistration_object.userId,
            URN=CIBRegistration_object.urn,
            ALIASID=CIBRegistration_object.aliasId
        )
