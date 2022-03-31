import abc
import socket
import ifaddr
from variables import domain
from bank_api import paytm
ipwhitelisting=False

server_ip = socket.gethostbyname(socket.gethostname())
bene_account_name = "SRS Live Technologies pvt Ltd"
bene_account_number="347505000468"
bene_ifsc = "ICIC0003475"
encrypted_password=False

# paytm_subwalletGuid = "4957c207-dafa-11eb-bbc6-fa163e429e83"
# paytm_merchant_id = "SubPai61513678214850"
# paytm_merchant_key = "@B0h97BGQ#YC_lIE"





# paytm_subwalletGuid = "4957c207-dafa-11eb-bbc6-fa163e429e83"
# paytm_merchant_id = "SubPai61513678214850"
# paytm_merchant_key = "@B0h97BGQ#YC_lIE"
def sms_api(phone_number,otp,name):
    
    return "https://api.msg91.com/api/sendhttp.php?sender=SPTRAN&route=4&mobiles="+phone_number+"&authkey=177009ASboH8XM59ce18cb&DLT_TE_ID=1107161794798561616&country=91&message=Dear,"+name+" otp :- "+otp+" Thanks. SabPaisa"
merchant_check=False
multitabs=False
AuthKey = "pMoG4Nsp54LGYV7a"
AuthIV = "4OqmI5rR7KOm6RmY"
admin_AuthKey="zDoSTQHGKAcQfYCY"
admin_AuthIV="BMifRscmnSWlnhmx"

paytm_link_transaction=paytm.staging_paytmPaymentAPI()
paytm_link_enquiry=paytm.staging_paytmEnquiryAPI()
paytm_subwalletGuid = "4957c207-dafa-11eb-bbc6-fa163e429e83"
paytm_merchant_id = "SubPai61513678214850"
paytm_merchant_key = "@B0h97BGQ#YC_lIE"
# paytm_merchant_id = "SRSLiv68510130188409"
# paytm_merchant_key = "hxsYuKDY6GP8S2Mr"
email_api = "https://adminapi.sabpaisa.in/REST/Email/sendEmail"

test_merchants=True
bank_ref_no = "1986517"
bank=11

