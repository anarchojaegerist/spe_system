from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User, Student, Coordinator

# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('title', 'given_names', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'given_names', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'title', 'given_names', 'last_name', 'is_staff')
    search_fields = ('email', 'given_names', 'last_name')
    ordering = ('email',)


admin.site.register(Student)
admin.site.register(Coordinator)