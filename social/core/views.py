from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from  . import models
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request,'index.html');

def signup(request):
    if(request.method=="POST"):
        username=request.POST['username']
        email1=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email1).exists():
                messages.info(request,'email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'user already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email1,password=password)
                user.save()
                
                user_model=User.objects.get(username=username)
                new_profile=models.Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request,'Password not matched')
            return redirect('signup')
    return render(request,'signup.html')

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin')
    return render(request,'signin.html');

def logout(request):
    auth.logout(request)
    return redirect('signin')