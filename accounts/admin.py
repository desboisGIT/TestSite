from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ( 'username', 'id','rank','email', 'full_name', 'country','tel', 'is_staff','mail_pro')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('full_name','rank', 'email', 'country','mail_pro')}),
        (('data'), {'fields': ('profile_picture', 'profile_free_text','darkTheme')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    
admin.site.register(CustomUser, CustomUserAdmin)

