from datetime import datetime
from tracemalloc import start
from venv import create
from pandas import to_datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from CustomDBLogger.models import StatusLog
from apis.serializersFolder.serializers import CustomLoggerSerializer
from apis.Utils import EmailAndSmsSender
import logging
from django.db.models import Q

logger = logging.getLogger('customLogger')


class CustomLoggerAPIView(APIView):

    def post(self, request):
        try:
            merchant_id = request.data.get('merchant_id',None)
            order_id = request.data.get('order_id', None)
            start= request.data.get('start', None)
            end= request.data.get('end', None)
            # create_datetime=request.data.get('create_datetime', None)
            pageno=5
            if merchant_id and order_id:
                qs = StatusLog.objects.filter(merchant_id=merchant_id, order_id=order_id, create_datetime__range=[start, end])[:pageno]
            elif start and end:
                qs=StatusLog.objects.filter(create_datetime__range=[start,end])
            else:
                qs = StatusLog.objects.all()
                print(qs)


                print(qs,"##############################")

            serializer = CustomLoggerSerializer(qs, many=True)
            # logger.info('Sending email')
            # EmailAndSmsSender.send_email("anand.rathore@sabpaisa.in", "TESTING", "TESTING")
            # EmailAndSmsSender.send_sms("9540514993", "TESTING")
            return Response(serializer.data)
        except Exception as e:
             return Response({"message":"error","response_code":"0"})