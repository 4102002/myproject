from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import pymongo
from .utils import get_db_handle
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
import json
from bson import json_util

# from django.core.mail import send_mail

# Create your views here.

db_handle, client = get_db_handle(db_name='drr',host="localhost",port=int(27017),username=None,password=None)
def createUser(request):
    db_handle, client = get_db_handle(db_name='drr',host="localhost",port=int(27017),username=None,password=None)
    if request.method == 'POST':
        username = request.POST['uEmail']
        password = request.POST['uPassword']
        firstname = request.POST['uFirstName']
        lastname = request.POST['uLastName']
        phone = request.POST['uPhone']
        createdAt = datetime.datetime.now()

        db_handle = client['drr']
        user = db_handle['users'].find_one({'username': username})
        if user is not None:
            return HttpResponse('User already exists')
        else:
            User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, phone=phone, createdAt=createdAt)
            db_handle['users'].insert_one({'username': username, 'password': password, 'firstname': firstname, 'lastname': lastname, 'phone': phone, 'createdAt': createdAt})
            return HttpResponse('success', status=200)
    else:
        return render(request, 'signup.html')
    
def user_auth(request):
    # db_handle, client = get_db_handle(db_name='drr',host="localhost",port=int(27017),username=None,password=None)

    if request.method == 'POST':
        username = request.POST.get('uEmail')
        password = request.POST.get('uPassword')
        db_handle = client['drr']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            user = db_handle['users'].find_one({'username': username, 'password': password})
            json_user = json.loads(json_util.dumps(user))
            get_user = User.objects.get(username=username)
            auth.login(request, get_user)
            request.session['user'] = json_user
            return HttpResponse('success')
        else:
            print('Invalid Credentials')
            return HttpResponse('Invalid Credentials')
    else:
        return render(request, 'login.html')
    
def logout(request):
    if auth.get_user(request).is_authenticated:
        auth.logout(request)
    try:
        del request.session['user']
    except:
        pass
    return HttpResponse('success', status=200)