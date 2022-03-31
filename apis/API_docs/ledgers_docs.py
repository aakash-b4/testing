from drf_yasg import openapi

fetch_request = openapi.Schema(
    # items=["trans_type","clientCode","orderId","startTime","endTime"],
    type=openapi.TYPE_OBJECT,
    properties={
        "property": openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    })


fetch_response_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message": "data found",
                "data": {
                    "balance": "balance",
                    "data": [
                        {
                            "id": "id",
                            "payoutTransactionId": "payout_txn_id",
                            "amount": "amount",
                            "transType": "type_type",
                            "statusType": "status_type",
                            "bankRefNo": "bank_ref",
                            "orderId": "order_id",
                            "beneficiaryAccountName": "beneficiary_account_name",
                            "beneficiaryAccountNumber": "beneficiary_account_number",
                            "beneficiaryIFSC": "beneficiary_ifsc",
                            "transStatus": "transaction_status",
                            "mode": "mode_id"
                        }
                    ]
                },
                "response_code": "1"
            }}
    ),
    "409": openapi.Response(
        description="custom 402 description",
        examples={
            "application/json": {
                "message": "some error",
                "error": "error args"
            }
        }
    ),

}
