from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserChangePasswordForm, UserSetResetPasswordForm,\
    UserCreationByAdminForm, UsersEditForm
# from django.forms import modelformset_factory
from django.contrib.auth import login, get_user_model, logout
from .models import Security
from django.contrib import messages
# from .utils import code_generator
# from django.contrib.auth.models import Group

from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


@login_required(login_url='/login')
def display_users_view(request, *args, **kwargs):
    if not request.user.is_club_admin and not request.user.is_staff:
        return HttpResponseRedirect("/home")
    user_qs = User.objects.all()
    userlist = []  # ikke akkurat standard django, men YOLO
    for user_object in user_qs:
        userlist.append(user_object)
    return render(request, "accounts/display_users.html", {'userlist': userlist})


@login_required(login_url='/login')
def edit_user_view(request, id=None, *args, **kwargs):
    if not id:
        return HttpResponseRedirect('/home')
    if not request.user.is_club_admin and not request.user.is_staff:
        return HttpResponseRedirect('/login')
    user_object_qs = User.objects.filter(id=id)
    if not user_object_qs.exists():
        return HttpResponseRedirect('/brukere')
    user_object = user_object_qs.first()
    form = UsersEditForm(request.POST or None, instance=user_object)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/brukere")
    return render(request, 'accounts/change_user.html', {'form': form})

# By Admin


@login_required(login_url='/login')
def register(request, *args, **kwargs):
    if (not request.user.is_club_admin) and (not request.user.is_staff):
        return HttpResponseRedirect('/login')
    form = UserCreationByAdminForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        from_email = settings.EMAIL_HOST_USER
        security_qs = Security.objects.filter(user=user_obj)
        html_message = ""
        if security_qs.exists() and security_qs.count() == 1:
            security_obj = security_qs.first()
            ps_key = security_obj.ps_key
            email = user_obj.email
            subject = "Velkommen " + user_obj.first_name + " " + user_obj.last_name
            msg = "Trykk på linken for å aktivere bruker"
            html_message += "<h3>Trykk på linken for å aktivere bruker<h3>"
            #Erstatt denne URL'en med nettsidens egen
            url = "http://127.0.0.1:8000/reset-password/" + ps_key
            html_message += '<a href="' + url + '"> Trykk her for å legge inn passord </a>'
            send_mail(subject=subject, from_email=from_email,
                      recipient_list=[email], message=msg, html_message=html_message)
            return HttpResponseRedirect("/brukere")

    return render(request, 'accounts/register.html', {"form": form})


def user_login(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email_ = form.cleaned_data.get('email')
        user_obj = User.objects.get(email__iexact=email_)
        login(request, user_obj)  # logger inn bruker i systemet
        if user_obj.is_club_admin:
            return HttpResponseRedirect("/home/admin/")  # to the page
        else:
            return HttpResponseRedirect("/home/clubofc/")
    return render(request, 'accounts/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/home")


def reset_password_mailer_view(request, *args, **kwargs):
    form = UserSetResetPasswordForm(request.POST or None)
    if form.is_valid():
        email_ = form.cleaned_data.get('email')
        user_obj = User.objects.get(email__iexact=email_)
        from_email = settings.EMAIL_HOST_USER
        security_qs = Security.objects.filter(user=user_obj)
        html_message = ""
        if security_qs.exists() and security_qs.count() == 1:
            security_obj = security_qs.first()
            ps_key = security_obj.ps_key
            subject = "tilbakestilling av passord"
            msg = "Hei, " + str(user_obj.get_name_of_user()) + ". Trykk på linken for å tilbakestille passord <br>"
            html_message += "<h3>Hei " +\
                            str(user_obj.get_name_of_user()) + ". Trykk på linken for å tilbakestille passord <h3> <br>"
            url = "http://127.0.0.1:8000/reset-password/"+ps_key
            html_message += '<a href="' + url + '"> Trykk her </a>'
            send_mail(subject=subject, from_email=from_email, recipient_list=[email_],
                      message=msg, html_message=html_message)
            return HttpResponseRedirect("/login")
    return render(request, "accounts/email_reset_password.html", {'form': form})


def set_password_view(request, code=None, *args, **kwargs):
    if code:
        security_qs = Security.objects.filter(ps_key=code)
        if security_qs.exists() and security_qs.count() == 1:
            security_obj = security_qs.first()
            user_obj = security_obj.user
            form = UserChangePasswordForm(request.POST or None, instance=user_obj)
            if form.is_valid():
                form.save()
                user_obj.is_active = True
                user_obj.save()
                login(request, user_obj)
                return HttpResponseRedirect("/home")
            return render(request, "accounts/reset_password.html", {'form': form})
    messages.warning(request, 'ugyldig kode eller allerde brukt')  # brukt opp
    return HttpResponseRedirect("/home/")
