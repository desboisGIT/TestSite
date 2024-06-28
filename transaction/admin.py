# accounts/admin.py

from django.contrib import admin
from .models import CompteBancaire, PayPalAccount

@admin.register(CompteBancaire)
class CompteBancaireAdmin(admin.ModelAdmin):
    list_display = ('user', 'cb_name', 'cb_number', 'cb_date')
    search_fields = ('cb_name', 'cb_number', 'user__id_user')
    list_filter = ('cb_date',)

@admin.register(PayPalAccount)
class PayPalAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'paypal_email')
    search_fields = ('paypal_email', 'user__id_user')

    def save_model(self, request, obj, form, change):
        if 'paypal_password_hash' in form.changed_data:
            obj.set_paypal_password(obj.paypal_password_hash)
        super().save_model(request, obj, form, change)

