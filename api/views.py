from django.shortcuts import render

from .dbcon import processquery
# Create your views here.
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .login_and_sign_up import handle_login
send_head = {
        "Access-Control-Allow-Origin" : "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers":"X-Requested-With, Content-Type",
        "Access-Control-Max-Age": "1000"
        }   

@api_view(['GET'])
def index(request):
    return HttpResponse("Hello, world. You're at home of api")

@api_view(['GET'])
def get_tc(request):
    tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM public.policy_data where policy_type = 1  order by policy_number asc")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)

@api_view(['GET'])
def get_privacy_policy(request):
    tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM public.policy_data where policy_type = 4  order by policy_number asc")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)

@api_view(['GET'])
def get_rev(request):
    tc_df = processquery("SELECT reviewer_name,review_text FROM public.review_master where should_been_shown = true")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)


@api_view(['POST'])
def login(request):
    headers = request.headers
    data = request.data
    phone_number = data['phone_number']
    password = data['password']
    user_id,message = handle_login(phone_number=phone_number,password=password)

    response = {"message_to_show":message,"user_id":user_id}
    if user_id != 0:
        send_head['user_id'] = user_id
    return Response(response,headers=send_head)
