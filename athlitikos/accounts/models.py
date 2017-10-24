#from django.db import models
from django.db.models.signals import post_save

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)
from django.conf import settings
from .utils import code_generator
from django.contrib.auth.models import Group

#Har basicly stjålet det meste fra django sin nettside:
#https://docs.djangoproject.com/en/1.11/topics/auth/customizing/
#Foretrekker dette alternativet, kan brukes til forenkling ect


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_club_admin = True
        user.save(using=self._db)

        #alternative security tokens
        #group = Group.objects.get(name='ClubAdmin')
        #user.groups.add(group)
        #group.save()

        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False) # en aktiv bruker
    is_club_admin = models.BooleanField(default=False) # klubb administrator godkjenner stevner ect
    is_staff = models.BooleanField(default=False) # for at man skal få adgang til /admin, var opprinelig en property
    is_admin = models.BooleanField(default=False) # database admininistrator
    objects = CustomUserManager()
    club = models.CharField(max_length=250, null=True)

    USERNAME_FIELD = 'email'

    #Hvis man skal kreve at bruker oppgir data til et spesifikk felt
    #REQUIRED_FIELDS = ['date_of_birth']
    #metoder som django krever
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_club_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

#    @property
#    def is_staff(self):
#        "Is the user a member of staff?"
#        # Simplest possible answer: All admins are staff
#        return self.is_admin


class Security(models.Model):#nøkklene brukes til å tilordne de forskjellige brukerene egenskaper
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activate_key = models.CharField(max_length=200)
    club_admin_key = models.CharField(max_length=200)
    ps_key = models.CharField(max_length=200)
    club_admin_key_used = models.BooleanField(default=False)
    def save(self,*args,**kwargs):
        self.club_admin_key = code_generator()# generer en tilfeldig alphanumerisk kode
        self.activate_key = code_generator()  # generer en tilfeldig alphanumerisk kode
        self.ps_key = code_generator()  # generer en tilfeldig alphanumerisk kode
        super(Security, self).save(*args, **kwargs)
    def __str__(self):
        return self.user.email

def post_save_user_model_receiver(sender,instance,created,*args,**kwargs): #knytter en bruker model mot aktivering som klubadministrator
    if created:
        try:
            Security.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)
