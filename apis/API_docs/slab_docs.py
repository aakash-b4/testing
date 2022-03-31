from drf_yasg import openapi
response={

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "message": "slab Added",
    "response_code": "1"
}
}
            

        
    ),
    "226":openapi.Response(
        description="custom 226 description",
        examples={
            "application/json": {
    "message": "slab for this merchant already exist",
    "response_code": "0"
}
}
            
  
    ),
    
   
}

request=openapi.Schema(
    # items=["trans_type","clientCode","orderId","startTime","endTime"],
    type=openapi.TYPE_OBJECT, 
    properties={
        "merchant_id":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    "min_amount":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    "max_amount":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    })
