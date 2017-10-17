#hvis alternativ 2, ps kan bruke begge to samtidig hvis ønskelig
from django.contrib import admin
#from .models import Profile

#admin.site.register(Profile)

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import UserChangeForm,UserCreationForm
from accounts.models import CustomUser,Security

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'club', 'is_admin', 'is_staff', 'is_club_admin', )
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('club',)}),
        ('Permissions', {'fields': ('is_admin','is_staff', 'is_club_admin')}),
        ('Access', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'club', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','club')
    ordering = ('club','email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Security)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)