from typing_extensions import Required
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserUpdateForm,ProfileUpdateForm

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, message
from django.template.loader import render_to_string
# Create your views here.

def loginuser(request):
    if request.method=="POST":
        form=AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/calc/posts/')
            else:
                messages.error(request, 'Invalid Username or password')
        else:
                messages.error(request, 'Invalid Username or password')  
    else:
        form=AuthenticationForm()
    return render(request, 'now/login.html',{'form':form})   

def logoutuser(request):
    logout(request) 
    messages.success(request, "successfully logout!")  
    return redirect('/calc/posts/')      

from .forms import SingUpForm
def registration(request):
    if request.method=="POST":
        form=SingUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            current_site=get_current_site(request)
            mail_subject='An account Created'
            message=render_to_string('now/account.html',{
                'user':user,
                'domain': current_site.domain
            })
            send_mail=form.cleaned_data.get('email')
            email=EmailMessage(mail_subject,message, to=[send_mail])
            email.send()
            messages.success(request,'Successfully created account')
            return redirect('login')
    else:
        form=SingUpForm   
    return render(request, 'now/singup.html',{'form':form})    

def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            update_session_auth_hash(request,form.user)
            messages.success(request,"Password has successfully Changed")
            return redirect('/calc/posts/')
    else:
        form=PasswordChangeForm(user=request.user)  
    return render(request, 'now/change_pass.html',{'form':form})


def profile(request):
    if request.method=="POST":
        u_form = UserUpdateForm(request.POST,  instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form':u_form,
        'p_form':p_form
            
    }
    return render(request, 'now/profile.html', context)


