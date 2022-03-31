from drf_yasg import openapi


response_login_request = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "message": "OTP sent ",
    "verification_token": "verification-token",
    "response_code": "1"
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

response_login_verification = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "auth-token": "auth-token",
    "jwt_token": {
        "refresh": "refresh token",
        "access": "access token"
    },
    "user_token": {
        "login_token": "login-token",
        "tab_login": "tab-token"
    },
    "response_code": "1"
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
        
    
    })


request_admin=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        
    
    })
verification=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        "otp":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    "geo_location":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
  "verification_code":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
  "type":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        
    
    })
resend_otp_request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
       
  "verification_code":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
  "type":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        
    
    })
# verification=openapi.Schema(
#     type=openapi.TYPE_OBJECT, 
#     properties={
#         {
#     "otp":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#     "geo_location":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
#     "verification_code":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
# }
    
#     })