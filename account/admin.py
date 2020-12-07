from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from account.models import User,Profile


class AccountAdmin(BaseUserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    readonly_fields = ('date_joined','last_login')
    search_fields = ('email','username')

    filter_horizontal = ()
    filter_vertical = ()
    fieldsets = ()
    

admin.site.register(User)
admin.site.register(Profile)
