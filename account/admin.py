from django.contrib import admin
from account.models import MyProfile, CustomUser
from account.form import  CustomUserForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User Post',
            {
                'fields':(
                    'is_manager',
                )
            }
        )
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(MyProfile)
