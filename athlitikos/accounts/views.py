from django.http import HttpResponseRedirect,HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, UserLoginForm,UserChangePasswordForm
from django.contrib.auth import login,get_user_model,logout
from .models import Security
from django.contrib import messages
from .utils import code_generator

User = get_user_model()

def club_official_options(request):

    # html = ''
    return HttpResponse()


@login_required(login_url='/login')
def admin(request):
    return render(request, 'accounts/admin.html')

def home(request):
    if request.user.is_authenticated():
        print(request.user.email)
    return render(request, "base.html", {})

def register(request,*args,**kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request,'accounts/register.html',{"form":form})

def user_login(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email_ = form.cleaned_data.get('email')
        user_obj = User.objects.get(email__iexact=email_)
        login(request,user_obj)#logger inn bruker i systemet
        return HttpResponseRedirect("/home2") #to the page
    return render(request,'accounts/login.html',{"form":form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login2")

def make_club_admin_view(request, code=None, *args,**kwargs):
    if code:
        security_qs = Security.objects.filter(club_admin_key=code)
        if security_qs.exists() and security_qs.count() == 1:
            security_obj = security_qs.first()
            if not security_obj.club_admin_key_used:
                user_obj = security_obj.user
                user_obj.is_club_admin = True
                user_obj.save()
                security_obj.club_admin_key_used = True
                security_obj.save()
                return HttpResponseRedirect("/login2") # suksess.
    messages.warning(request,'ugyldig kode eller allerde brukt') #brukt opp
    return HttpResponseRedirect("/home2",)

def activate_user(request, code=None, *args,**kwargs):
    if code:
        security_qs = Security.objects.filter(activate_key=code)
        if security_qs.exists() and security_qs.count() == 1:
            security_obj = security_qs.first()
            user_obj = security_obj.user
            user_obj.is_active = True
            user_obj.save()
            security_obj.save()
            return HttpResponseRedirect("/login2")  # suksess.
    messages.warning(request, 'ugyldig kode eller allerde aktiv')  # brukt opp
    return HttpResponseRedirect("/home2",)



def reset_password_view(request, code=None, *args,**kwargs):
    if code:
        security_qs = Security.objects.filter(ps_key=code)
        if security_qs.exists() and security_qs.count() == 1:
            security_obj = security_qs.first()
            user_obj = security_obj.user
            form = UserChangePasswordForm(request.POST or None, instance=user_obj)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/home2")
            return render(request, "accounts/reset_password.html", {'form':form})
    messages.warning(request, 'ugyldig kode eller allerde brukt')  # brukt opp
    return HttpResponseRedirect("/home2", )