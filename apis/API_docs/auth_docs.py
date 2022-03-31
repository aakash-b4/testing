from drf_yasg import openapi
admin_response_dict={

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "Message": "user created",
    "response_code": "1",
    "user_id": "user_id",
    "CLIENT_AUTH_KEY": "auth_token",
    "CLIENT_AUTH_IV": "auth_iv",
    "token": {
        "refresh": "refresh-token",
        "access": "access-token"
    }
}
            

        }
    ),
    "409": openapi.Response(
        description="custom 402 description",
        examples={
            "application/json":{
    "message": "some error",
    "error":"error args"
}
        }
    ),
   
}
response_schema_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "message": "user created",
    "merchant_id":"client merchant id",
    "response_code": "1",
    "CLIENT_AUTH_KEY": "client auth key",
    "CLIENT_AUTH_IV": "client auth iv",
    "token": {
        "refresh": "refresh token",
        "access": "access token"
    }
}
            

        }
    ),
    "409": openapi.Response(
        description="custom 402 description",
        examples={
            "application/json":{
    "message": "some error",
    "error":"error args"
}
        }
    ),
   
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        "email":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        "client_id":openapi.Schema(type=openapi.TYPE_INTEGER, description='client id'),
        "client_code":openapi.Schema(type=openapi.TYPE_STRING, description='client code'),
        "bank_code":openapi.Schema(type=openapi.TYPE_INTEGER, description='string'),
        "role_id":openapi.Schema(type=openapi.TYPE_INTEGER, description='integer'),
        "ip_addresses":openapi.Schema(type=openapi.TYPE_ARRAY, description='array',items="string"),
        "phone_number":openapi.Schema(type=openapi.TYPE_INTEGER, description='string')
    
    })

request_admin=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
     "username":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
     "name": openapi.Schema(type=openapi.TYPE_STRING, description='string'),
     "password":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
     "email":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
     "role_id":openapi.Schema(type=openapi.TYPE_INTEGER, description='integer'),
     "phone_number":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    
    })

# request_admin=openapi.Schema(
#     type=openapi.TYPE_OBJECT, 
#     properties={
#         {
#     "username":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#     "name": openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#     "password":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#     "email":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#     "role_id":openapi.Schema(type=openapi.TYPE_INTEGER, description='integer'),
#     "phone_number":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
# }}
    
    
#     )