from pickle import TRUE
import traceback
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework.response import Response
from rest_framework import status

from apis.database_service import Log_model_services
from apis.serializersFolder.serializers import CibRegistrationSerializer
from apis.database_models.CIBRegistrationModel import CIBRegistration
from apis.bank_models.ICICI_Model.CIBRegistrationResponseModel import CIBRegistrationResponse
from apis.bank_models.ICICI_Model.CIBRegistrationRequestModel import CIBRegistrationRequestModel
from .. import const
import json
from apis.bank_services.ICICI_service import utils
from apis.bank_conf.config import Configuration
from sabpaisa import auth


class CIBRegistrationAPIView(APIView):
    def post(self, request):
        print("========= inside cib_registration =========")
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="cib registration "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const. server_ip, full_request=request_obj)
        log_id = log.save()
        try:
            header = request.headers.get("auth_token")
            if header is None:
                return Response({"message": "auth_token is missing"}, status=status.HTTP_400_BAD_REQUEST)
            merchantId = auth.AESCipher(
                const.AuthKey, const.AuthIV).decrypt(header)
        except:
            traceback.print_exc()
            return Response({"message": "Invalid Auth Token"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CibRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # fetch the aggrId, userId, corpId, aggrName from the request
            aggrId = serializer.validated_data['aggrId']
            userId = serializer.validated_data['userId']
            corpId = serializer.validated_data['corpId']
            aggrName = serializer.validated_data['aggrName']
            bank = serializer.validated_data['bank']
            serializer.validated_data['merchantId'] = merchantId
            # check the existence of data in the database for cib registration
            cib_registration_obj = None
            try:
                cib_registration_obj = CIBRegistration.objects.get(
                    aggrId=aggrId, userId=userId, corpId=corpId, aggrName=aggrName, bank=bank, merchantId=merchantId)
            except CIBRegistration.DoesNotExist:
                print("cib registration does not exist")
            if cib_registration_obj:
                if str(cib_registration_obj.status).lower() == "true":
                    return Response(cib_registration_obj.to_json(), status=status.HTTP_200_OK)
                if not serializer.equals(cib_registration_obj, serializer.validated_data):
                    print("cib registration data is not same")
                    cib_registration_obj.aggrId = serializer.validated_data['aggrId']
                    cib_registration_obj.userId = serializer.validated_data['userId']
                    cib_registration_obj.corpId = serializer.validated_data['corpId']
                    cib_registration_obj.aggrName = serializer.validated_data['aggrName']
                    cib_registration_obj.bank = serializer.validated_data['bank']
                    cib_registration_obj.merchantId = serializer.validated_data['merchantId']
                    cib_registration_obj.urn = serializer.validated_data['urn']
                    cib_registration_obj.merchantAccountNumber = serializer.validated_data['merchantAccountNumber']
                    cib_registration_obj.save()
            else:
                cib_registration_obj = serializer.save()
            request_model = CIBRegistrationRequestModel.from_CIBRegistration(
                cib_registration_obj)
            qs = vars(request_model)
            request_data = utils.create_icici_request(qs)
            response = utils.send_request(url=Configuration.get_Property(
                'ICICI_CibRegistrationURL'), data=request_data, type="POST")
            try:
                bank_response = response.json()
                if 'encryptedKey' in bank_response:
                    bank_response = json.loads(
                        utils.decrypt_data(bank_response))
                cib_registration_obj.response = bank_response.get(
                    'response', None)
                cib_registration_obj.status = bank_response.get('status', None)
                cib_registration_obj.success = bank_response.get('success', None)
                cib_registration_obj.message = bank_response.get('message', None)
                cib_registration_obj.errorCode = bank_response.get(
                    'errorCode', None)
                cib_registration_obj.errorMessage = bank_response.get(
                    'errormessage', None)
                if cib_registration_obj.success:
                    cib_registration_obj.status = True
                else:
                    cib_registration_obj.status = False
                cib_registration_obj.save()
                return Response(cib_registration_obj.to_json(), status=status.HTTP_200_OK)
            except Exception as e:
                print("<===== exception in cib registration =====> ")
                traceback.print_exc()
                bank_response = response.text
                cib_registration_obj.response = response.text
                cib_registration_obj.save()
            Log_model_services.Log_Model_Service.update_response(
                log_id, bank_response)
            return Response(bank_response)
        else:
            return Response(serializer.errors)




