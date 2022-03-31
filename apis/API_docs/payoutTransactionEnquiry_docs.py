from drf_yasg import openapi

response_schema_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message":"data found",
                "resData": "Encrypted Data",
                "response_code":"1"
            },
            

        }
    ),
    "404":openapi.Response(
        description="custom 401 description",
        examples={
            "application/json":{"message":"NOT_FOUND","response_code":"0"}
        }
    )
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'auth-token(header)': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'query': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    })