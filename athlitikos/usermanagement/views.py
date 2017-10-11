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

    def post(self, request):
        pass



