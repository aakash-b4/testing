import ast
import random
import re

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from apis.database_models.PayeeMasterModel import *
import base64
import requests
import json
from sabpaisa import auth
from tabulate import tabulate
import uuid
import datetime


# from config import ICICIConfiguration
# from icici.models import UpiPaymentRequest


def createPaymentRequestPayload(json: dict) -> dict:
    # delete p_mode from json
    if 'p_mode' in json:
        del json['p_mode']
    keys = list(json.keys())
    for key in keys:
        if '_' in key:
            json[key.replace('_', '-')] = json[key]
            del json[key]
    return json


# Function to generate 16 character random string
def generate_random_number():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(16))


# Function to encrypt data using RSA/ECB/PKCS1 padding and public key
def encrypt_data(data):
    print("========================== Encrypting data ==========================")
    random_number = generate_random_number()
    response = {}
    keyPub = RSA.import_key(
        open("cert/UAT_CIB.txt", "r").read())
    # open("icici/cert/test/STAR_sabpaisa_in.txt", "r").read())
    keyPub = keyPub.publickey().exportKey()
    publicKey = str(keyPub.decode().replace(
        '-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').replace('\n', ''))
    # publicKey = str(open("icici/cert/test/paymentkey.txt", "r").read())
    jsonData = {
        "data": "",
        "rsaKey": publicKey,
        "aesKey": random_number
    }
    res = requests.post('http://localhost:8081/encryptData',
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(jsonData))
    encKey = res.json().get('encKey')
    response['encryptedKey'] = encKey
    IV = generate_random_number()
    DATA = str(IV) + data

    # encrypt DATA using AES/CBC/PKCS5 padding using random_number as key and random2 as iv
    key = str(random_number).encode()
    print("key = ", key)
    iv = str(IV).encode()
    print("iv = ", iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # pad data
    print("data = ", DATA)
    padded_data = pad(str(DATA).encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encrypted_data_base64 = base64.b64encode(encrypted_data)
    response['encryptedData'] = encrypted_data_base64.decode()
    print("========================== Encryption done ==========================")
    return response


def composite_data_encrypt(data):
    print("========================== Encrypting data ==========================")
    random_number = generate_random_number()
    response = {}
    keyPub = RSA.import_key(
        open("cert/Composite-UAT.txt", "r").read())
    # open("icici/cert/test/STAR_sabpaisa_in.txt", "r").read())
    keyPub = keyPub.publickey().exportKey()
    publicKey = str(keyPub.decode().replace(
        '-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '').replace('\n', ''))
    # publicKey = str(open("icici/cert/test/paymentkey.txt", "r").read())
    jsonData = {
        "data": "",
        "rsaKey": publicKey,
        "aesKey": random_number
    }
    res = requests.post('http://localhost:8081/encryptData',
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(jsonData))
    encKey = res.json().get('encKey')
    response['encryptedKey'] = encKey
    IV = generate_random_number()
    DATA = str(IV) + data

    # encrypt DATA using AES/CBC/PKCS5 padding using random_number as key and random2 as iv
    key = str(random_number).encode()
    print("key = ", key)
    iv = str(IV).encode()
    print("iv = ", iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # pad data
    print("data = ", DATA)
    padded_data = pad(str(DATA).encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    encrypted_data_base64 = base64.b64encode(encrypted_data)
    response['encryptedData'] = encrypted_data_base64.decode()
    print("========================== Encryption done ==========================")
    return response


# Function to decrypt data using RSA/ECB/PKCS1 padding and private key
def decrypt_data(data):
    print("========================== Decrypting data ==========================")
    private_key = open("cert/star.sabpaisa.in.key", "r").read()
    jsonData = {
        "rsaKey": private_key,
        "data": data['encryptedKey']
    }
    res = requests.post('http://localhost:8081/decryptData',
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(jsonData))
    print("Decryption response >>> ", res.json())
    decKey = res.json().get('decKey')
    enc_data = base64.b64decode(data['encryptedData'])
    iv = enc_data[:16]
    cipher = AES.new(decKey.encode(), AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(enc_data), AES.block_size)
    data = decrypted_data[16:].decode()
    print("decrypted data : ", data)
    print("========================== Decryption done ==========================")
    return data


def create_icici_request(qs):
    print("plain request data : ", json.dumps(qs, default=str))
    request_data = encrypt_data(json.dumps(qs, default=str))
    request_data['requestId'] = generate_random_number()[:10]
    request_data['service'] = 'CIB'
    request_data['iv'] = ''
    request_data['clientInfo'] = ''
    request_data['optionalParam'] = ''
    request_data['oaepHashingAlgorithm'] = 'NONE'
    print("encrypted request data : ", json.dumps(request_data))
    return request_data


def create_icici_composite_request(qs):
    print("plain request data : ", json.dumps(qs, default=str))
    request_data = composite_data_encrypt(json.dumps(qs, default=str))
    request_data['requestId'] = generate_random_number()[:10]
    request_data['service'] = 'CIB'
    request_data['iv'] = ''
    request_data['clientInfo'] = ''
    request_data['optionalParam'] = ''
    request_data['oaepHashingAlgorithm'] = 'NONE'
    print("encrypted request data : ", json.dumps(request_data))
    return request_data


def send_request(url, data, headers={}, type="POST"):
    # add content type, accept and other headers
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    headers['apikey'] = 'VS9vDBOtyGHx0SvQl5ww3AUILUKjHyAj'
    print("sending request...")
    if type == 'POST':
        res = requests.post(url, json=data, headers=headers)
    elif type == 'GET':
        res = requests.get(url, json=data, headers=headers)
    else:
        res = requests.post(url, json=data, headers=headers)
    print("request sent")
    log_request(res)
    return res


# Function to log the request and response


def log_request(response):
    print("======================= request details begin =======================")
    print("status code : ", response.status_code)
    print("type : ", response.request.method)
    print("URL : ", response.request.url)
    # print request headers using for loop
    print("<------------------- request headers begins --------------------------->")
    print(tabulate(response.request.headers.items(),
                   headers=['key', 'value'], tablefmt="fancy_grid"))
    print("<------------------- request headers ends --------------------------->")
    print("body : ", response.request.body.decode())
    print("response body : ", response.text)
    print("===================== request details end ============================")


def validate_name(name: str):
    if len(name) < 2:
        return {"status": False, "message": "Name should have atleast 2 characters"}
    if not re.match("^[a-zA-Z ]*$", name):
        return {"status": False, "message": "Name should contain only alphabets"}
    return {"status": True, "message": "Name is valid"}


def validate_account_number(account_number: str):
    if len(account_number) < 9:
        return {"status": False, "message": "Account number should be of 9 digits"}
    if not re.match("^[0-9]*$", account_number):
        return {"status": False, "message": "Account number should be of numeric characters"}
    return {"status": True, "message": "Account number is valid"}


def verify_account_number(account_number: str, ifsc: str, merchant_id: str):
    try:
        acc_detail = PayeeMasterModel.objects.get(account_number=account_number, ifsc=ifsc, merch_id=merchant_id)
        if acc_detail.isActive == "N":
            return {"status": False, "message": "Beneficiary is disabled."}
        if acc_detail.ifscAlreadyAdded == "Y":
            return {"status": False, "message": "Beneficiary is already added."}
    except Exception as e:
        print(e)
        return {"status": False, "message": "Account number and IFSC is invalid. Please verify."}
    return {"status": True, "message": "Beneficiary Details are valid"}


def validate_upi_id(upi_id: str):
    if "@" not in upi_id:
        return {"status": False, "message": "UPI ID should be in proper format"}
    return {"status": True, "message": "UPI ID is valid"}


def verify_upi_id(upi_id: str, merchant_id: str):
    try:
        acc_detail = PayeeMasterModel.objects.get(upi_id=upi_id, merch_id=merchant_id)
        if acc_detail.isActive == "N":
            return {"status": False, "message": "Beneficiary is disabled."}
        if acc_detail.upiAlreadyAdded == "Y":
            return {"status": False, "message": "Beneficiary is already added."}
    except Exception as e:
        print(e)
        return {"status": False, "message": "UPI Id is invalid. Please verify."}
    return {"status": True, "message": "UPI ID is valid"}


def validate_amount(amount: str):
    if not re.match("^[0-9]*[.][0-9]{2}$", amount):
        return {"status": False, "message": "Amount should be of numeric characters with two decimal places"}

    converted_amount = ast.literal_eval(amount)
    if not isinstance(converted_amount, float):
        print("converted amount : ", converted_amount)
        return {"status": False, "message": "Amount should be in decimal format"}

    if converted_amount <= 0:
        return {"status": False, "message": "Amount should be greater than 0"}
    return {"status": True, "message": "Amount is valid"}


def validate_order_id(order_id: str):
    if len(order_id) < 5:
        return {"status": False, "message": "Order id should have atleast 5 characters"}
    if not re.match("^[a-zA-Z0-9]*$", order_id):
        return {"status": False, "message": "Order ID should not contain any special characters"}

    return {"status": True, "message": "Order ID is valid"}


def validate_ifsc(amount: str):
    if not re.match("^[A-Z]{4}0[A-Z0-9]{6}$", amount):
        return {"status": False, "message": "Invalid IFSC code"}

    # method to generate seq-no


def generate_seq_no() -> str:
    return "ICI" + str(uuid.uuid4()).replace("-", "")


# method to generate random number
def generate_order_id():
    return str(uuid.uuid4())[:8].replace("-", "")


# method to get concatenated date string
def get_concatenated_local_date():
    return str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
