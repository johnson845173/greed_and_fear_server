from django.shortcuts import render

from .dbcon import processquery
# Create your views here.
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

@api_view(['GET'])
def index(request):
    return HttpResponse("Hello, world. You're at home of api")

@api_view(['GET'])
def get_tc(request):

    tc_df = processquery("SELECT policy_number,policy_heading,policy_text FROM public.policy_data where policy_type = 1")

    tc_json =tc_df.to_json(orient='index')

    tc_json = json.loads(tc_json)

    return Response(tc_json)

