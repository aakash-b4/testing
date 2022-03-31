from drf_yasg import openapi
response_dict={

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
       "data_length": 1,
    "data": "encrypted_data"
    }
}
            

        
    ),
    
   
}

request=openapi.Schema(
    # items=["trans_type","clientCode","orderId","startTime","endTime"],
    type=openapi.TYPE_OBJECT, 
    properties={
        "start":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    "end":openapi.Schema(type=openapi.TYPE_STRING, description='string')
    })
