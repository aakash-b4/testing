from drf_yasg import openapi

response_schema_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message":"data parsed and saved to database",
                "response_code":"1"
            }
        }
    )
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'auth-token(header)': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'files': openapi.Schema(type=openapi.TYPE_STRING, description='excelfile'),
    })



fetch_request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
    "account_number":"account_number",
    "ifsc_code":"ifsc_code"
})
single_bene=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'auth-token(header)': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'query': openapi.Schema(type=openapi.TYPE_STRING, description='excelfile'),
    })
single_bene_response={

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
               "msg":"data saved to database","response_code":'1'
            }
        }
    )
}
fetch_response={

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "data":"Encrypted data",
    "responseCode":"1",
}
        }
    )
}

fetch_request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        "query":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    })


