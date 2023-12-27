from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from  . import models
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=models.Profile.objects.get(user=user_object)
    posts=models.Post.objects.all();
    return render(request,'index.html',{'user_profile':user_profile,'posts':posts});

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
                #log user in and redirect settings page
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                #create a profile model for the user
                user_model=User.objects.get(username=username)
                new_profile=models.Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
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

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile=models.Profile.objects.get(user=request.user)
    if request.method=="POST":
        if request.FILES.get('image')==None:
            image = user_profile.profimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        else:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')    
    return render(request,'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method=="POST":
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']
        
        new_post=models.Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('index')
    else:
        return redirect('index')

@login_required(login_url='signin')  
def like(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    post=models.Post.objects.get(id=post_id)
    like_filter=models.LikePost.objects.filter(post_id=post_id,username=username).first()
    
    if like_filter==None:
        new_like=models.LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('index')
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('index')
  
@login_required(login_url='signin')  
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=models.Profile.objects.get(user=user_object)
    user_posts=models.Post.objects.filter(user=pk)
    length=len(user_posts)
    context={
        'user_profile':user_profile,
        'user_object':user_object,
        'user_posts':user_posts,
        'length':length
    }
    return render(request,'profile.html',context)
