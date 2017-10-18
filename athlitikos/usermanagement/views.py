from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.generic import View
from .forms import UserForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group


class UserFormView(View):
    form_class = UserForm
    template_name = 'newuser.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            status = form.cleaned_data['status']
            user.set_password(password)
            user.save()

            if(status == "1"):

                group = Group.objects.get(name='Admin')
                user.groups.add(group)
                group.save()

            if(status == "2"):

                group = Group.objects.get(name='ClubOfficial')
                user.groups.add(group)
                group.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('/home')

        return render(request, self.template_name, {'form': form})


def club_official_options(request):
    # html = ''
    return HttpResponse()


@login_required(login_url='/login')
def admin(request):
    return render(request, 'admin.html')


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')
