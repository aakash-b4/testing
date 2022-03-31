

class UpiPaymentStatus():
    def __init__(self, date = None, recon360 = None, seq_no = None, channel_code = None, ori_seq_no = None, mobile = None, profile_id = None, device_id = None):
        self.date = date
        self.recon360 = recon360
        self.ori_seq_no = ori_seq_no
        self.channel_code = channel_code
        self.seq_no = seq_no
        self.mobile = mobile
        self.profile_id = profile_id
        self.device_id = device_id

    # to_Json method
    def to_Json(self):
        return {
            "date": self.date,
            "recon360": self.recon360,
            "ori_seq_no": self.ori_seq_no,
            "channel_code": self.channel_code,
            "seq_no": self.seq_no,
            "mobile": self.mobile,
            "profile_id": self.profile_id,
            "device_id": self.device_id
        }

    def from_Json(self, json):
        self.date = json.get('date', None)
        self.recon360 = json.get('recon360', None)
        self.ori_seq_no = json.get('ori_seq_no', None)
        self.channel_code = json.get('channel_code', None)
        self.seq_no = json.get('seq_no', None)
        self.mobile = json.get('mobile', None)
        self.profile_id = json.get('profile_id', None)
        self.device_id = json.get('device_id', None)