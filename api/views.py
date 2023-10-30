from django.shortcuts import render

from .dbcon import processquery,engine,text
# Create your views here.
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from . import otp_handler
from rest_framework import status
from pdf_generation import main,simple
import os
from .login_and_sign_up import handle_login,log_user
from .telegram_message import send_message
import time
from minio import Minio
from . import dbcon
from . import whatsapp_test
from . import nse_handler
import datetime

import threading

send_head = {
        "Access-Control-Allow-Origin" : "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS,POST",
        "Access-Control-Allow-Headers":"*",
        "Access-Control-Max-Age": "1000",
        'X-Requested-With':'XMLHttpRequest'
        }   

@api_view(['GET'])
def index(request):
    return Response({"message":"Success9"},headers=send_head)

@api_view(['GET'])
def clear_db(request):
    query = """select 
    pg_terminate_backend(pid)
    from pg_stat_activity
    where state = 'idle' and usename = 'appsmith'"""
    dbcon.excute_query(query=query)
    return Response({"message":"sucess"})

@api_view(['GET','POST'])
def log_user_view(request):
    log_user(request=request)
    return Response({"message":"Success7"},headers=send_head)

@api_view(['GET'])
def get_intra_stock(request):
    # tc_df = processquery("SELECT stockname,img_path FROM public.stock_master where to_be_displayed = true")
    # tc_json =tc_df.to_json(orient='records')
    # response = json.loads(tc_json)

    client = Minio(
        endpoint="s3.greedandfear.fun",
        access_key="miniopython",
        secret_key="O9FNbVbZVD47cEgiAb8nH8548l0ZqYh2b7q61m9L"
    )

    # Make 'asiatrip' bucket if not exist.
    # obj = client.get_presigned_url(bucket_name="stock",object_name="logo.jpg",method="GET")

    tc_json = []
    stocks = client.list_objects(bucket_name="stock")
    for each_stock in stocks:
        url = client.get_presigned_url(method="GET",bucket_name="stock",object_name=each_stock.object_name)

        tc_json.append(
            {   
                "stockname":" ",
                "img_path":url
            }
        )

    print(tc_json)
    response = json.loads(json.dumps(tc_json))
    
    return Response(response,headers=send_head)

@api_view(['GET'])
def get_indices_stock(request):   
    client = Minio(
        endpoint="s3.greedandfear.fun",
        access_key="miniopython",
        secret_key="O9FNbVbZVD47cEgiAb8nH8548l0ZqYh2b7q61m9L"
    )

    # Make 'asiatrip' bucket if not exist.
    # obj = client.get_presigned_url(bucket_name="stock",object_name="logo.jpg",method="GET")

    tc_json = []
    stocks = client.list_objects(bucket_name="indices")
    for each_stock in stocks:
        url = client.get_presigned_url(method="GET",bucket_name="indices",object_name=each_stock.object_name)
        tc_json.append(
            {   
                "stockname":" ",
                "img_path":url
            }
        )

    response = json.loads(json.dumps(tc_json))
    
    return Response(response,headers=send_head)



@api_view(['GET'])
def get_tc(request):
    log_user(request=request)
    tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM policy.policy_data where policy_type = 1  order by policy_number asc")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)

@api_view(['GET'])
def get_privacy_policy(request):
    log_user(request=request)
    tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM policy.policy_data where policy_type = 4  order by policy_number asc")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)

@api_view(['GET'])
def get_rev(request):
    log_user(request=request)
    tc_df = processquery("SELECT reviewer_name,review_text,logo_path FROM public.review_master where should_been_shown = true order by display_order asc")
    tc_json =tc_df.to_json(orient='records')
    response = json.loads(tc_json)
    return Response(response,headers=send_head)


@api_view(['POST'])
def login(request):
    headers = request.headers
    data = request.data
    phone_number = data['phone_number']
    password = data['password']
    user_id,message,status_code = handle_login(phone_number=phone_number,password=password)

    response = {"message_to_show":message,"user_id":user_id}
    if user_id != 0:
        send_head['user_id'] = user_id
    return Response(response,headers=send_head,status=status_code)


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
    
    query = text(f"""INSERT INTO management.preorder_data(
	user_name, email, phone, basic, premium, elite, elloit_wave, fibbonaci)
	VALUES (:user_name, :email, :phone, :basic, :premium, :elite, :elloit_wave, :fibbonaci);""")
    query = query.bindparams(user_name=user_name, email=email, phone=phone, basic=basic, premium=premium, elite=elite, elloit_wave=ew, fibbonaci=fib)
    engine.execute(query)
    response = {"message_to_show":"Added"}
    return Response(response,headers=send_head)


@api_view(['GET'])
def sample_pdf(request,file_name):
    # data = request.data

    # file_name = data['file_name']
    file_name = file_name

    obj = main.Student_login(file_name=file_name)

    obj.main()

    print("PDF Gen")
    # time.sleep(5)

    file_path = f"../shared_pdf/{file_name}.pdf"

    with open(file_path, 'rb') as f:
           file_data = f.read()

    response = HttpResponse(file_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + f"{file_name}.pdf" + '"'
    return response

@api_view(['GET'])
def simple_pdf(request,file_name):
    # data = request.data

    # file_name = data['file_name']
    file_name = file_name

    obj = simple.Student_login(file_name=file_name)

    obj.main()

    print("PDF Gen")
    # time.sleep(5)

    file_path = f"../shared_pdf/{file_name}.pdf"

    with open(file_path, 'rb') as f:
           file_data = f.read()

    response = HttpResponse(file_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + f"{file_name}.pdf" + '"'
    return response

@api_view(['GET'])
def view_pdf(request,file_name):
    # data = request.data

    # file_name = data['file_name']
    file_name = file_name

    file_name = file_name

    obj = simple.Student_login(file_name=file_name)

    obj.main()

    print("PDF Gen")

    
    file_path = f"../shared_pdf/{file_name}.pdf"

    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    print("Path Exist")

    response = HttpResponse(file_data, content_type='application/pdf')
    response["Access-Control-Allow-Methods"]= "GET, OPTIONS,POST"
    response["Access-Control-Allow-Headers"]="*"
    response["Access-Control-Max-Age"]= "1000"
    response['X-Requested-With']='XMLHttpRequest'
    response["Access-Control-Allow-Origin"] = "*"
    response["X-Frame-Options"] = "SAMEORIGIN"
    response['Content-Disposition'] = 'inline; filename="' + f"{file_name}.pdf" + '"'
    return response

@api_view(['POST'])
def send_reminder(request):
    headers = request.headers
    data = request.data
    user_id = data['user_id']
    whatsapp_test.send_sub_renew_message(user_id=user_id)
    response = {"message_to_show":"Sucess","user_id":user_id}
    return Response(response,headers=send_head,status=200)



@api_view(['GET'])
def update_sebi_bans_view(request):
    nse_handler.get_oi_sebi()
    nse_handler.get_sebi_bans()
    return Response({"message":"Success"},headers=send_head)

@api_view(['GET'])
def get_sebi_bans_view(request):

    query_parameter = request.query_params

    date_to_compare = query_parameter.get('date_to_compare',datetime.datetime.today().strftime("%Y-%m-%d"))

    date_of_trade = query_parameter.get('date_of_trade',(datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    data = nse_handler.get_nse_bans_from_data_base(date_to_compare=date_to_compare,date_of_trade=date_of_trade)

    return Response({"message":"Success","data":data},headers=send_head)

@api_view(['POST'])
def send_whatspp_otp_view(request):
    try:
        phone_number = request.data.get("phone_number")

        otp = otp_handler.set_otp(phone_number=phone_number)

        whatsapp_test.send_whatsapp_otp_message(phone_number=phone_number,otp=otp)

        return Response({"message":"Success"},headers=send_head,status=status.HTTP_200_OK)
    except:
        return Response({"message":"Failed"},headers=send_head,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def validate_whatspp_otp_view(request):
    try:
        phone_number = request.data.get("phone_number")

        user_otp = request.data.get("user_otp")

        validation_sucess_json = otp_handler.validate_otp(phone_number=phone_number,user_otp=user_otp)
        
        return Response(data=validation_sucess_json,headers=send_head,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"Failed","error":str(e)},headers=send_head,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
