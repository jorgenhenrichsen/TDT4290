from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
#from accounts.models import CustomUser works but not django convention

#this gets the user model regardless of customization
from django.contrib.auth import authenticate,get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Epost")
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs): #to only the form
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            raise forms.ValidationError("feil epost eller passord")#wrong email
        else:
            if not user_obj.check_password(password):
                #log aut tries
                raise forms.ValidationError("feil epost eller passord")#wrong ps
        #our_user = authenticate(email=email, password=password)
        #if not our_user:
        #    raise forms.ValidationError("feil epost eller passord") #does the same as code above


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','club')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangePasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user_obj = self.instance
        user_obj.set_password(self.cleaned_data["password1"])
        if commit:
            user_obj.save()
        return user_obj
    class Meta:
        model = User
        #må eksludere mange felt så ikke dette kan endres av bruker
        exclude = ('email', 'club', 'is_active', 'is_admin','is_staff','password', 'is_club_admin', 'last_login')


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'club', 'is_active', 'is_admin','is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
