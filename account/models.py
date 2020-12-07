from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("username is required")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
  
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password=None):

        user = self.create_user(
            email= email,
            password=password,
            username=username,

        ) 
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 
    

class User(AbstractUser):
    email           = models.CharField(verbose_name='email',max_length=50,unique=True)
    username        = models.CharField(max_length=100,null=True,unique=True,help_text="Username must be unique try with numbers too")
    date_joined     = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login',auto_now= True)
    is_admin        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self,prem,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True


def profile_photo_upload_location(instance, filename):
	file_path = 'profile_photo/{username}/{filename}'.format(
				username=str(instance.user.username), filename=filename)
	return file_path


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(auto_now_add=False,blank=True,null=True)
    profile_photo = models.ImageField(upload_to=profile_photo_upload_location, blank=True)
    seld_description = models.TextField(blank=True,null=True,max_length=500)

    def __str__(self):
        return f"Profile for - {self.user.username}"