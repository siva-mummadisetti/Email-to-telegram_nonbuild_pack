from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User  # direct way of creating user

import easyimap
import json # built-in

from .models import User

def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email_password = request.POST["email_password"]
        if(len(username)>0 and len(password)>0 and len(email_password)>0):
            user = authenticate(request, username = username, password = password)
        else:
            return render(request, "Email/login.html",{
                "message2": "info: Please fill all the fields."
            })
        if user is not None:
            login(request, user)
            temp = User.objects.get(username = request.user.username)
            temp.emailPassword = email_password
            temp.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "Email/login.html",{
                "message1": "Error: Invalid username and/or password."
            })
    else:
        return render(request, "Email/login.html")

def logoutView(request):
    try:
        temp = User.objects.get(username = request.user.username)
        temp.emailPassword = ""
        temp.save()
        logout(request)
        return render(request, "Email/login.html",{
            "message2": "Successfully logged out..."
        })
    except Exception:
        return HttpResponseRedirect(reverse('login'))

def registerView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        email_id = request.POST["email_id"]
        telegram_id = request.POST["telegram_id"]
        if(len(username)>0 and len(password)>0 and len(confirm_password)>0 and len(email_id)>0 and len(telegram_id)):
            if telegram_id[0] != '@':
                telegram_id = '@'+telegram_id
            if password != confirm_password:
                return render(request, "Email/register.html",{
                    "message1": "Error: password != Confirm password"
                })
        else:
            return render(request, "Email/register.html",{
                "message2": "info: Please fill all the fields."
            })
        try:
            user = User.objects.create_user(username = username,email = email_id,password = password, emailPassword = "", telegramId = telegram_id, reqCount = 0 )
            user.save()
        except IntegrityError:
            return render(request, "Email/register.html", {
                "message2": "info: Username already taken."
            })
        except ValueError:
            return render(request, "Email/register.html",{
                "message2": "info: Please fill all the fields."
            })
        
        return render(request, "Email/login.html",{
            "message2": "Account created successfully, Please login..."
        })
    else:
        return render(request, 'Email/register.html')

def about(request):
    return render(request, 'Email/about.html')


def index(request):
    if request.user.is_authenticated:
        sender = []
        sub = []
        email_id = request.user.email
        email_password = request.user.emailPassword
        telegram_id = request.user.telegramId
        temp = request.user.reqCount = request.user.reqCount+1
        request.user.save()
        domain = email_id[((email_id.index('@'))+1):]
        host = f"imap.{domain}"
        try:
            server = easyimap.connect(host, email_id, email_password)
        except Exception:
            logout(request)
            return render(request, "Email/login.html",{
                "message1": "Error: Invalid email id and/or email password",
                "message3": "info: This error will also show up if you haven’t been given access to Less Secure Apps",
                "message4": "to give access and try again.",
                "message2": "Info: If you think I have given the wrong email id, Please create another account and continue..."
            })
        unread_emails = server.unseen(limit = 2)
        for email in unread_emails:
            sender.append(email.from_addr)
            sub.append(email.title)
        data = list(zip(sub, sender))
        json_data_array = json.dumps(data)  # json objects(array, Object, numbers, string...) json.dumps() used to convert py lis to js array and py dict to js Object
        # json.loads() converts js Object to py dict, js array to py list...
        json_data_string = json.dumps(telegram_id)
        server.quit()

        return render(request, 'Email/index.html',{
            "data" : json_data_array,
            "telegram_id" : json_data_string,
            "reqCount" : temp
        })
    else:
        return HttpResponseRedirect(reverse("login"))

