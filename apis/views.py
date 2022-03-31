from django.http.response import HttpResponse
from .view_api import auth,beneficiary,extras,ledger,login,logs,payout,test,charge,slab,client,dailyLedger,IpWhitelisting,merchantMode,webhook,bankpartner,Role, icici

from threading import Thread


# class Ledger_Updater(Thread):
#     def run(self):
#         pass

# Ledger_Updater().start()

def testicici(request):
    import requests
    # from crypto.PublicKey import RSA
    # from crypto.Cipher import PKCS1_v1_5
    from base64 import b64decode,b64encode
    api_link="https://apibankingsandbox.icicibank.com/api/v1/composite-payment/"
    api_key="VS9vDBOtyGHx0SvQl5ww3AUILUKjHyAj"
    compose_api="https://apibankingsandbox.icicibank.com/api/v1/composite-status/"
    composite_val="https://apibankingsandbox.icicibank.com/api/v1/composite-validation/"
    beni_api="https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/BeneAddition"

    key="""MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAsIwVStQi6aSMLBZu3vha
    fOR5NTMNp+TXPwyk/6VoaSQfDnZaSQPYhdt4a8X215KwXwpIL1eBJOH2NW8jp5AO
    4WauHWEwEggJvPaC8FgzZtDhjYexOk+/yaDbY7U9BofJSU76VIBxRoN7YmAknAKr
    pfn0ukXPPuUx5Ny/cy85nunqo5M8Acf2VVwSGZQMBZFSm3yxYOdS4laDlM+s1w+5
    wLDMjYSgIMm76rpVdO3hs2n2dSAYM6XMOaqNDwHdZk006n8lPgivYVXjTz7KU9eqkF
    necWvn2ugRI7hgrplZxS020k0QBeYd0AH7zJZKS3Xo5VycL01UO/WYOQvB7v8lge
    7TiQZ3CCrnuykqcJ/r5DMLO/cKQAeZi+LQ95FQg39joO8G7bfO7+a3Gs8Re3mRW7
    AA8x1aEn7XZMOUu4l4IfNvwh20V4cz3xvGXdr9ZLFvgX5593MxCDBjkiaynzG8gm
    LVTIoaItPy+khwO/vjfWka0L3yvT3l55R4H/KRKxlHaY58HVdLbuWrUoH/4gbkYF
    YFC+rejBW5wbE0FJmWIkEXLKsTlXcsn6eAzi4BRxidQ/4rIEf8qWpSFzJobivBnW
    e4bpBA19g3N47PDpD5xS6uj7ODSBhEn22UnsiDaGV+RhsXYA/xqaJCjB6+W7CN00
    Lowr87sUoT4VAK8wrOk4D5sCAwEAAQ=="""

    upi={
    "mobile": "7000000023",
    "device-id": "190160190160190160190160",
    "seq-no": "5DC866EA6ADC427",
    "account-provider": "74",
    "payee-va": "moto2.4@icici",
    "payer-va": "uat@icici",
    "profile-id": "2995692",
    "amount": "1.00",
    "pre-approved": "P",
    "use-default-acc": "D",
    "default-debit": "N",
    "default-credit": "N",
    "payee-name": "MEHUL",
    "mcc": "6011",
    "merchant-type": "ENTITY",
    "txn-type": "merchantToPersonPay",
    "channel-code": "MICICI",
    "remarks": "none",
    "crpID" : "API3",
    "aggrID" : "AGGR0008",
    "userID" : "USER2",
    "vpa":"moto2.4@icici"
    }

    key1="0OQMsS1x49HQ6fP2"
    iv="7y9xWwHc6OVLv5oM"

    json={

    "requestId": "",

        "service": "UPI",

        "encryptedKey": "<<ENCR_KEY>>",

        "oaepHashingAlgorithm": "NONE",

        "iv": "",

        "encryptedData": "<<ENCR_DATA>>",

        "clientInfo": "",

        "optionalParam": ""

    }
    json1={
    "requestId": "",
    "service": "PaymentApi",
    "encryptedKey":
    """oG5mU1JJNBuwQaSLKb3wfRZks/cT2Vo2yBNNuqjNHDWEC144WxC8iKqBpJAgq7reFKC4sHNUmNPRDya1AvmQ7x1L+3EA
    dEs9FEWNurZuWTvZpk4y7JrGhg0rz9KptBf+JfJUkSMo7NR3Saxel6EYtckkDr3AGW7WJZmhcEoAMMXRws/hLVmaNHC/nOj
    CNqqBd4IOOAzdJh/HADRVI+YAJKT8dE4x9NTl+UX1zAooWhza+TsWEHfxzQIa7zai7WSa/wiJD3uD7mk5vT1WY/fKJBquCuz
    M7l35vigDhmb7dLVLuX8VMiNQrtErWNI0uVaag1jg+uZUtyDSxjPFi5yEpKVVc7+T503IDnCvkCFDygqasDsPL24qOjYk4XavTZv
    wGuPAdYNNkVnLzVElEhg4zS2ye+fa/8fZiMt/3fwYeN9dgn9i5R6VOFbXSuZJYPSci9k0oqz73h1nzFtps60rUEDoGIkGvm9waJ
    U3W78VH5mIdGfGvvJjiKIuVHmi/huzEX9v4w3mW7RDGgmOuKImkqki+XWgyB0JvVmsLdO+cBaym/seZP3+zdfhO9AWSI2t
    DLD4Vf0jDjzoDSFN2mzUFgHK9mbtbXgvsnReoGqx/KsivzmZNLmDm tg8eR4Z9LnLni4rl4OtkDv5y/mxMtL3MBUUUajkw6OS
    6NnhEG895yo=""",
    "oaepHashingAlgorithm": "NONE",
    "iv": "",
    "encryptedData":
    """wBJSefFsnJVlobh1cJR553w6Ay6b8/2frCjxvdZ1Bsnxztsul7Ha8lFl4PoZD+IhdlRShWdKgz3yJYIisGV/KKpyMSY3DILOpbkqEa
    0Qq0g=""",
    "clientInfo": "",
    "optionalParam": ""
    }
    benijson={
    "CrpId" : "PRACHICIB1",
    "CrpUsr":"USER3",
    "BnfName" : "AnshumanMishra",
    "BnfNickName" : "Ansh",
    "BnfAccNo" : "000405001257",
    "PayeeType" : "W",
    "IFSC" : "ICIC0000011",
    "AGGR_ID" : "CUST0589",
    "URN" : "3kCy4sPuSqDNi4kggXJIoE568221"
    }

    # def rsa_encrypt(s):
    #     key = b64decode(public_key)
    #     key = RSA.importKey(key)

    #     cipher = PKCS1_v1_5.new(key)
    #     ciphertext = b64encode(cipher.encrypt(bytes(s, "utf-8")))

    #     return ciphertext
    uat_endpoint="https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/BeneAddition"
    response = requests.post(uat_endpoint,json=benijson,headers={"api-Key":"VS9vDBOtyGHx0SvQl5ww3AUILUKjHyAj"})
    # response=requests.post(api_link,json=upi,headers={'apikey':api_key,'x-priority':"1000",'content-type':"application/json"}, verify='CER - CRT Files/AAACertificateServices.crt')
    return HttpResponse(response)
    #print(response.json())
