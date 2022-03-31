from drf_yasg import openapi

response_schema_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message":"Payout done",
                "resData": "Encrypted Data",
                "response_code":"1"
            },
            

        }
    ),
    "402": openapi.Response(
        description="custom 402 description",
        examples={
            "application/json": {"message":"Not Sufficent Balance or Beneficary not matched","response_code":"0"}
        }
    ),
    "401":openapi.Response(
        description="custom 401 description",
        examples={
            "application/json":{"message":"credential not matched","response_code":"3"}
        }
    ),
    "204":openapi.Response(
        description="custom 204 description",
        examples={
            "application/json":{"message":"error msg","response_code":"2"}
        }
    ),
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'auth-token(header)': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'encrypted_code': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        "mode":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    })