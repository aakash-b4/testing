from apis.database_models.SlabModel import SlabModel
from apis.database_service.Slab_model_services import Slab_Model_Service
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..API_docs import slab_docs
from .. import const
import sabpaisa
from ..database_models import BOUserModel
from ..serializersFolder.serializers import SlabSerializer
class SlabView(APIView):

    @swagger_auto_schema(request_body=slab_docs.request,responses=slab_docs.response)
    def post(self,req):
        try:
            admin_id = req.headers['auth_token']
            admin_id=sabpaisa.auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(admin_id)
            if len(BOUserModel.BOUserModel.objects.filter(id=admin_id))<=0:
                return Response({"message":"UNAUTHORISED"})
            merchant_id = req.data["merchant_id"]
            max_amount = req.data["max_amount"]
            min_amount = req.data["min_amount"]
            slabview = Slab_Model_Service(merchant_id=merchant_id,min_amount=min_amount,max_amount=max_amount)
            if slabview.save()==None:
                return Response({"message":"slab for this merchant already exist","response_code":"0"},status=status.HTTP_226_IM_USED)
            return Response({"message":"slab Added","response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"message":"some Technical Error","Response_code":"2",},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchSlab(APIView):
    def post(self,req):
        try:
            admin_id = req.headers['auth_token']
            admin_id=sabpaisa.auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(admin_id)
            if len(BOUserModel.BOUserModel.objects.filter(id=admin_id))<=0:
                return Response({"message":"UNAUTHORISED"})
            merchant_id=req.data['merchant_id']
            slab = Slab_Model_Service.fetch_by_merchant_id(merchant_id)
            ser=SlabSerializer(slab,many=True)
            return Response({"data":ser.data})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"message":"some Technical Error","Response_code":"2",},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeleteSlab(APIView):
    def post(self,req):
        try:
            admin_id = req.headers['auth_token']
            admin_id=sabpaisa.auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(admin_id)
            if len(BOUserModel.BOUserModel.objects.filter(id=admin_id))<=0:
                    return Response({"message":"UNAUTHORISED"})
            Slab_Model_Service.delete_slab(req.data["id"])
            return Response({"message":"Slab Deleted","response_code":200},status=status.HTTP_200_OK)
        except Exception as e:
                import traceback
                print(traceback.format_exc())
                return Response({"message":"some Technical Error","Response_code":"2",},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateSlab(APIView):
    def post(self,req):
        try:
            admin_id = req.headers['auth_token']

            admin_id=sabpaisa.auth.AESCipher(const.admin_AuthKey,const.admin_AuthIV).decrypt(admin_id)
            if len(BOUserModel.BOUserModel.objects.filter(id=admin_id))<=0:
                    return Response({"message":"UNAUTHORISED"})
            model=req.data["slab"]
            slab=SlabModel()
            slab.min_amount=model['min_amount']
            slab.max_amount=model['max_amount']
            slab.merchant_id=model['merchant_id']
            
            Slab_Model_Service.update_slab(slab)

            return Response({"message":"Slab updated","response_code":200},status=status.HTTP_200_OK)
        except Exception as e:
                import traceback
                print(traceback.format_exc())
                return Response({"message":"some Technical Error","Response_code":"2",},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

