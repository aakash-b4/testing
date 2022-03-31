from django import http
from django.shortcuts import redirect
def val(req):
    return redirect("api/")
# def uiTest(req):
#     return http.HttpResponse("some")