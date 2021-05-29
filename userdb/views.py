from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from . models import User_Data

import json

from django.views.decorators.csrf import csrf_exempt


def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

@api_view()
def add_user(request):
    print(request.query_params)
    if request.method == 'GET':
        state = request.query_params['state']
        age = request.query_params['age']
        available_capacity = request.query_params['dose']
        district = request.query_params['district']
        toaddr = request.query_params['email']
        if(int(available_capacity)== 1):
            available_capacity = '_dose1'
        elif(int(available_capacity)== 2):
            available_capacity = '_dose2'
        else:
            return HttpResponse("invalid dose value", content_type='text/json')

        user = User_Data(state=state,age=int(age),available_capacity=available_capacity,district=district,toaddr=toaddr)
        try:
            user.save()
            response = json.dumps([{ 'Success': 'Added Info Successfully,You will be notified ASAP!'}])
        except:
            response = json.dumps([{ 'Error': 'Info could not be added!'}])
    return HttpResponse(response, content_type='text/json')

def get_user(request):
    if request.method == 'GET':
        try:
            users_list = User_Data.objects.all()
            return_list =[]
            if users_list:
              for i in (users_list):
                return_list.append({'toaddr': i.toaddr, 'age': i.age,'state':i.state,'district':i.district,'available_capacity':i.available_capacity,'user_id':i.user_id})
            response = json.dumps(return_list)
        except:
            response = json.dumps([{ 'Error': 'Info couldn"t be fetched'}])
    return HttpResponse(response, content_type='text/json')