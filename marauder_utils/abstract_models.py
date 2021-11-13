from django_currentuser.db.models import CurrentUserField
from django.db import models


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    created_by = CurrentUserField(related_name="%(app_label)s_%(class)s_created_by")
    updated_date = models.DateTimeField(auto_now=True,null=True)
    updated_by = CurrentUserField(on_update=True,related_name="%(app_label)s_%(class)s_updated_by")

    class Meta:
        abstract = True

    objects = models.Manager()