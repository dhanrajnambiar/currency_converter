from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

import requests, re, json
from django.contrib.auth.models import User
from .models import client
from .forms import RegForm, convertForm, loginForm


# Create your views here.

def app_home(request):
    intro_text = "This is a currency converter application. App let's you convert between USD, INR, SGD, GBP, EUR by the live rates. Kindly register to use the app OR login if registered!!!"

    context = {
        'text':intro_text,
    }

    return render(request, 'converter/app_home.html', context)

def signup(request):
    form_var = RegForm(request.POST or None)
    heading = "SignUp"
    if request.method == 'POST':
        if form_var.is_valid():
            form_var.save(commit = False)
            usrname = form_var.cleaned_data.get('username')
            pwd = form_var.cleaned_data.get('password1')
            User.objects.create_user(username = usrname, password = pwd)
            user_to_login = authenticate(username = usrname, password = pwd)
            if user_to_login is not None:
                login(request, user_to_login)
                return redirect('user_home', username = usrname)

    context = {
        'form':form_var,
        'title':heading,
    }

    return render(request, 'converter/signup.html', context)

def login_user(request):
    form_var = loginForm(request.POST or None)
    heading = "LOGIN"
    pwd_flag = False#set true if wrong passsword entered
    if request.method == "POST":
        if form_var.is_valid():
            usr_name = form_var.clean_username()
            pwd = form_var.clean_password()
            usr = authenticate(username = usr_name, password = pwd)
            if usr is not None:
                    login(request, usr)
                    return redirect('user_home', username = usr_name)
            else:
                #print("inputted wrong password")
                pwd_flag = True

    if pwd_flag:
        alert_msg = "Username or Password is Incorrect.Please enter correct login details!!!"
    else:
        alert_msg = None

    context = {
        'msg':alert_msg,
        'form':form_var,
        'title':heading,
    }

    return render(request, 'converter/login.html', context)


def logout_user(request):
    logout(request)
    text = "Thank You, Visit Again!!!"
    context = {
        'title':text,
    }

    return render(request, 'converter/logout.html', context)


def homepage(request, username):
    welcome_note = "Welcome " + str(username)
    form_var = convertForm(request.POST or None)

    def conv(curr_from,curr_to,much):
        if curr_from != curr_to:
            r = requests.get("http://api.fixer.io/latest?base=%s" % curr_from)
            s = r.content.decode()#converting to text from byte file retruned by api
            data = json.loads(s)#converting to json format |||lr to dict data type
            return round((data['rates'][curr_to] * much), 3)
        else:
            return much

    if request.user.is_authenticated:
        x = User.objects.get(username = username)
        a = client.objects.get(user = x)
        trans_hist = a.list_transactions()

        if request.method == "GET":
            context = {
                'trans_list': trans_hist,
                'title':welcome_note,
                'form':form_var,
            }

        if request.method == "POST":
            selected_1 = request.POST.get('field1')
            selected_2 = request.POST.get('field2')
            val_to_convert = request.POST.get('field3')
            if selected_1 != selected_2:
                result = conv(selected_1,selected_2, float(val_to_convert))
            else:
                result = val_to_convert

            res_str = selected_1 + ' to ' + selected_2 + ' ' + val_to_convert + ' result: ' + str(result)
            a.add_transactions(res_str)

            context = {
                'result':result,'title':welcome_note,'form':form_var,'from':selected_1,'to':selected_2,'val':val_to_convert,'trans_list':trans_hist,
            }

    else:
        return redirect('user_login')

    return render(request, 'converter/users_home.html', context)
