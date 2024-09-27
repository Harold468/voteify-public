from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
# Create your models here.
import os

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        email = self.normalize_email(email)
        user = self.model(email =email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,email,password,**extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_admin',True)

        user = self.create_user(email,password,**extra_fields)

        return user
        




class USERMODEL(AbstractBaseUser,PermissionsMixin):

    class Meta:
        verbose_name='USER'
        verbose_name_plural='USERS'
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    phone = models.CharField(max_length=255,unique=True)
    organization = models.CharField(max_length=255,default='Unknown')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    


class EVENT(models.Model):

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    name_of_event = models.CharField(max_length=255)
    event_organizer = models.ForeignKey(USERMODEL,on_delete=models.CASCADE)
    event_picture = models.FileField(upload_to='event_picture/',null=True,blank=True)
    event_code  = models.CharField(max_length=255,null=True,blank=True)
    paid = models.BooleanField(default=False)
    amount = models.DecimalField(default=2.00,max_digits=20,decimal_places=2)
    total_balance = models.DecimalField(default=0.00,max_digits=20,decimal_places=2)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()

    def delete(self,*args, **kwargs):

        if self.event_picture:
            if os.path.isfile(self.event_picture.path):
                os.remove(self.event_picture.path)
        super().delete(*args,**kwargs)


    def __str__(self):
        return f'{self.name_of_event.title()} by {self.event_organizer}'

    




