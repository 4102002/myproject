from django.shortcuts import render
from django.http import HttpResponse
import pymongo
from .utils import get_db_handle
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from gridfs import GridFS
import os
import pandas as pd
import numpy as np
import bson
import json
import datetime
import time
import re
import csv
import sys
import math
import random
import string
import traceback
# from django.core.mail import send_mail

# Create your views here.
db_handle, client = get_db_handle(db_name='drr',host="localhost",port=int(27017),username=None,password=None)

def get_client_ip_city(request):
    client_ip, city = None, None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')

    return client_ip, city

@login_required
def home(request):
    ip, city = get_client_ip_city(request)
    print(f"IP: {ip}, City: {city}")
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        try:
            uploaded_file = request.FILES['file']
            db_handle = client['drr']
            collection = db_handle['users']
            fs = GridFS(db_handle)
            # Store file in MongoDB and file metadata in a users collection
            fs_id = fs.put(uploaded_file, filename=uploaded_file.name)
            fs_name = fs.get(fs_id).filename
            collection.update_one({'username': request.user.username}, {'$push': {'files': [fs_id,fs_name]}})
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failure'})
    else:
        return JsonResponse({'status': 'failure'})

def get_file_description(request):
    try:
        db_handle = client['drr']
        fs = GridFS(db_handle)
        filename = request.GET['file']
        file = fs.get_last_version(filename=filename)
        file_description = {}
        
        df = pd.read_csv(file)
        rows, columns = df.shape
        file_description['filename'] = filename
        file_description['size_in_kb'] = str(round(file.length/1024, 2))
        file_description['file_type'] = filename.split('.')[-1]
        file_description['rows'] = rows
        file_description['columns'] = columns
        file_description['column_names'] = list(df.columns)
        file_description['column_types'] = [str(i) for i in list(df.dtypes)]
        file_description['column_nulls'] = [str(df[i].isnull().sum() )for i in list(df.columns)]
        file_description['column_unique'] = [str(len(df[i].unique()) )for i in list(df.columns)]
        numeric = [i for i in list(df.columns) if df[i].dtype in [np.int64, np.float64]]
        file_description['numeric_columns'] = [i for i in list(df.columns) if df[i].dtype in [np.int64, np.float64]]
        file_description['column_max'] = [str(round(df[i].max(),2)) for i in numeric]
        file_description['column_min'] = [str(round(df[i].min(),2)) for i in numeric]
        file_description['column_mean'] = [str(round(df[i].mean(),2)) for i in numeric]
        file_description['column_median'] = [str(round(df[i].median(),2)) for i in numeric]
        file_description['column_mode'] = [str(round(df[i].mode()[0],2)) for i in numeric]
        file_description['column_std'] = [str(round(df[i].std(),2)) for i in numeric]
        file_description['column_skew'] = [str(round(df[i].skew(),2)) for i in numeric]
        return JsonResponse({'status': 'success', 'data': file_description})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'failure'})

def get_files(request):
    try:
        db_handle = client['drr']
        collection = db_handle['users']
        user = collection.find_one({'username': request.user.username})
        files = user['files']
        fs = GridFS(db_handle)
        file_list = []
        for file in files:
            file_list.append(fs.get(file).filename)
        return JsonResponse({'files': file_list})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failure'})

def download_file(request):
    try:
        db_handle = client['drr']
        fs = GridFS(db_handle)
        file = fs.get(request.GET['file'])
        response = HttpResponse(file.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % request.GET['file']
        return response
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failure'})
    
def delete_file(request):
    try:
        db_handle = client['drr']
        collection = db_handle['users']
        fs = GridFS(db_handle)
        file = fs.get(request.GET['file'])
        fs.delete(file._id)
        collection.update_one({'username': request.user.username}, {'$pull': {'files': request.GET['file']}})
        return JsonResponse({'status': 'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'failure'})




# def sendmail(request):
#     FROM = "drrsystem66@gmail.com"
#     TO = "meetprajapati20@gnu.ac.in"
#     SUBJECT = "Hello!"
#     TEXT = "This message was sent with Python's smtplib."
    
#     # Send mail
#     send_mail(SUBJECT, TEXT, FROM, [TO])
