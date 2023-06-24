from django.shortcuts import render

from .dbcon import processquery,engine,text
# Create your views here.
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .login_and_sign_up import handle_login,log_user
from .telegram_message import send_message

send_head = {
        "Access-Control-Allow-Origin" : "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS,POST",
        "Access-Control-Allow-Headers":"X-Requested-With, Content-Type, Accept, Origin, Authorization",
        "Access-Control-Max-Age": "1000"
        }   

@api_view(['GET'])
def index(request):
    return HttpResponse("Hello, world. You're at home of api")

@api_view(['GET','POST'])
def log_user_view(request):
    log_user(request=request)
    return Response({"message":"Success"},headers=send_head)

@api_view(['GET'])
def get_intra_stock(request):
    tc_df = processquery("SELECT stockname,img_path FROM public.stock_master where to_be_displayed = true")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)



@api_view(['GET'])
def get_tc(request):
    log_user(request=request)
    tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM public.policy_data where policy_type = 1  order by policy_number asc")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)

@api_view(['GET'])
def get_privacy_policy(request):
    log_user(request=request)
    tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM public.policy_data where policy_type = 4  order by policy_number asc")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)

@api_view(['GET'])
def get_rev(request):
    log_user(request=request)
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


@api_view(['GET','POST'])
def razorpay_update(request):
    headers = request.headers
    data = request.data
    mesage = {"data":data,"headers":headers}
    send_message(message=str(mesage))
    response = {"message":"Success"}

    return Response(response,headers=send_head)

@api_view(['POST'])
def preorder(request):
    headers = request.headers
    data = request.data
    user_name = data['user_name']
    email = data['email']
    phone = data['phone']
    basic = data['basic']
    premium = data['premium']
    elite = data['elite']
    ew = data['ew']
    fib = data['fib']
    
    query = text(f"""INSERT INTO public.preorder_data(
	user_name, email, phone, basic, premium, elite, elloit_wave, fibbonaci)
	VALUES (:user_name, :email, :phone, :basic, :premium, :elite, :elloit_wave, :fibbonaci);""")
    query = query.bindparams(user_name=user_name, email=email, phone=phone, basic=basic, premium=premium, elite=elite, elloit_wave=ew, fibbonaci=fib)
    engine.execute(query)
    response = {"message_to_show":"Added"}
    return Response(response,headers=send_head)

{
"user_name":"johnson",
"email":"johnson@email",
"phone":7899345443,
"basic":"true",
"premium":"true",
"elite":"true",
"ew":"true",
"fib":"false"
}