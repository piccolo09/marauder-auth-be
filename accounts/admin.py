from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.utils.translation import ugettext_lazy as _
from .models import User


class AdminUserCreationForm(UserCreationForm):
    """
        Custom Create Form for user creation
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

class AdminUserChangeForm(UserChangeForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = '__all__'
        # field_classes = {'username': UsernameField}

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (_("Basic Info"), {
            'classes': ('collapse', ),
            'fields': ('email', 'password','first_name','last_name','inviter')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active', 'is_staff','activated',
                    'is_superuser', 'groups',
                    'user_permissions')
            }
        ),
        (_('Important dates'), {'fields': ('created_by','created_date', 'updated_date','updated_by', 'last_login')}),
    )
    readonly_fields = ('created_date', 'updated_date', 'last_login','updated_by','created_by')
    add_fieldsets = (
        (_("Basics"), {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2', ),
        }),
    )
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    list_display = ('email', 'is_staff', 'is_active','first_name', 'last_name')
    ordering = ('email',)