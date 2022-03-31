from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework.response import Response
from rest_framework import status
from sabpaisa import auth

class EncryptView(APIView):
    def post(self, request):
        #fetch authKey and authIV from the request or else assign empty string
        authKey = request.data.get("authKey") or "1QD08ceLckopU5Ja"
        authIV = request.data.get("authIV") or "i3t2bpBSK07HfdFj"
        query = ""
        for key, value in request.data.items():
            # concat key and value to query using &
            query = query + key + "=" + value + "&"
        # remove the last & from query
        query = query[:-1]
        query = auth.AESCipher(authKey, authIV).encrypt(query)
        print(query)
        return Response({"query": query}, status=status.HTTP_200_OK)

class DecryptView(APIView):
    def post(self, request):
        #fetch authKey and authIV from the request or else assign empty string
        authKey = request.data.get("authKey") or "1QD08ceLckopU5Ja"
        authIV = request.data.get("authIV") or "i3t2bpBSK07HfdFj"
        query = request.data.get("query")
        query = auth.AESCipher(authKey, authIV).decrypt(query)
        # split the query using & and store it in a list
        query_list = query.split("&")
        # create a dictionary to store the key and value
        query_dict = {}
        for item in query_list:
            # split the item using = and store it in a list
            item_list = item.split("=")
            # store the key and value in the dictionary
            query_dict[item_list[0]] = item_list[1]      
        return Response(query_dict, status=status.HTTP_200_OK)