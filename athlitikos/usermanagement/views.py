from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import ClubOfficial
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic, View
from .forms import UserForm
from django.shortcuts import render, redirect

@login_required(login_url='/login')
def admin(request):
    return render(request, 'admin.html')

def create_new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'newuser.html', {'form': form})

class UserFormView(View):

    form_class = UserForm
    template_name = 'newuser.html'

    #Display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form' : form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #Returns user object if credentials are correct
            user = authenticate(username=username, password=password)

            if user.is_active:

                login(request, user)
                request.user
                return redirect('http://127.0.0.1:8000/admin-startside/')

        return render(request, self.template_name, {'form' : form})



