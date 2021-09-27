from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserAccount
# Register your models here.
# admin.site.unregister(User)
admin.site.register(UserAccount)
