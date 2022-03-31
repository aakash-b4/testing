
from bank_api import run_java, icici


class Header_Request:
    def __init__(self, Username="", Password=""):
        self.Username = Username
        self.Password = Password

    def to_Json(self):
        return {
            "Username": self.Username,
            "Password": run_java.runJavaCode(self.Password.strip(), icici.key())
        }


class IciciUpiPaymentRequest:
    def __init__(self, vpa=None, mobile=None, device_id=None,
                 seq_no=None,
                 account_provider=None,
                 payee_va=None,
                 payer_va=None,
                 profile_id=None,
                 amount=None,
                 pre_approved=None,
                 use_default_acc=None,
                 default_debit=None,
                 default_credit=None,
                 payee_name=None,
                 mcc=None,
                 merchant_type=None,
                 txn_type=None,
                 channel_code=None,
                 remarks=None,
                 crpID=None,
                 aggrID=None,
                 userID=None):
        self.vpa = vpa
        self.mobile = mobile
        self.device_id = device_id
        self.seq_no = seq_no
        self.account_provider = account_provider
        self.payee_va = payee_va
        self.payer_va = payer_va
        self.profile_id = profile_id
        self.amount = amount
        self.pre_approved = pre_approved
        self.use_default_acc = use_default_acc
        self.default_debit = default_debit
        self.default_credit = default_credit
        self.payee_name = payee_name
        self.mcc = mcc
        self.merchant_type = merchant_type
        self.txn_type = txn_type
        self.channel_code = channel_code
        self.remarks = remarks
        self.crpID = crpID
        self.aggrID = aggrID
        self.userID = userID

    # to_Json method
    def to_Json(self):
        return {
            "vpa": self.vpa,
            "mobile": self.mobile,
            "device_id": self.device_id,
            "seq_no": self.seq_no,
            "account_provider": self.account_provider,
            "payee_va": self.payee_va,
            "payer_va": self.payer_va,
            "profile_id": self.profile_id,
            "amount": self.amount,
            "pre_approved": self.pre_approved,
            "use_default_acc": self.use_default_acc,
            "default_debit": self.default_debit,
            "default_credit": self.default_credit,
            "payee_name": self.payee_name,
            "mcc": self.mcc,
            "merchant_type": self.merchant_type,
            "txn_type": self.txn_type,
            "channel_code": self.channel_code,
            "remarks": self.remarks,
            "crpID": self.crpID,
            "aggrID": self.aggrID,
            "userID": self.userID
        }

    # function to convert json to class object
    @staticmethod
    def from_Json(json_object):
        return IciciUpiPaymentRequest(
            vpa=json_object.get("vpa", None),
            mobile=json_object.get("mobile", None),
            device_id=json_object.get("device_id", None),
            seq_no=json_object.get("seq_no", None),
            account_provider=json_object.get("account_provider", None),
            payee_va=json_object.get("payee_va", None),
            payer_va=json_object.get("payer_va", None),
            profile_id=json_object.get("profile_id", None),
            amount=json_object.get("amount", None),
            pre_approved=json_object.get("pre_approved", None),
            use_default_acc=json_object.get("use_default_acc", None),
            default_debit=json_object.get("default_debit", None),
            default_credit=json_object.get("default_credit", None),
            payee_name=json_object.get("payee_name", None),
            mcc=json_object.get("mcc", None),
            merchant_type=json_object.get("merchant_type", None),
            txn_type=json_object.get("txn_type", None),
            channel_code=json_object.get("channel_code", None),
            remarks=json_object.get("remarks", None),
            crpID=json_object.get("crpID", None),
            aggrID=json_object.get("aggrID", None),
            userID=json_object.get("userID", None)
        )
