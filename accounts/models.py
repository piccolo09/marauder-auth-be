
from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager, PermissionsMixin
from django.db.models.query_utils import select_related_descend
# Create your models here.

# Creating users
class UserAccountManager(BaseUserManager):
    
    def create_user(self,email,password=None,is_admin=False,is_staff=False,is_active=False): #,username,address,
        if not email:
            raise ValueError("User Must Have Email ")
        if not password:
            raise ValueError("Password is required")
        email = self.normalize_email(email)
        user = self.model(email=email)  #username=username,address=address
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active 
        user.save(self._db)
        return user

    def create_staffuser(self,email,password=None): #,username,address
        email = self.normalize_email(email)
        user = self.model(email=email,password=password)
        user.staff = True
        user.active=True 
        user.save(using=self._db)
        return user

    
    def create_superuser(self,email,password=None):
        email = self.normalize_email(email)
        user = self.model(email=email,password=password)
        user.staff = True    
        user.admin = True
        user.active=True 
        user.save(using=self._db)
        return user


class UserAccount(AbstractUser):
    email = models.EmailField(max_length=255,unique=True)
    address = models.TextField(blank=True,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','address']

    # def get_full_name(self):
    #     return self.email

    # def get_short_name(self):
    #     return self.email

    # def __str__(self):
    #     return self.email
    

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.staff

    # @property
    # def is_admin(self):
    #     "Is the user a admin member?"
    #     return self.admin

    # @property
    # def is_active(self):
    #     return self.active