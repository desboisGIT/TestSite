from django.db import models
import bcrypt

from accounts.models import CustomUser


class CompteBancaire(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # One-to-many relationship
    cb_name = models.CharField(max_length=255)
    cb_number = models.CharField(max_length=50, unique=True)  # Assuming account number is unique
    cb_code = models.CharField(max_length=50)
    cb_date = models.DateField()
    class Meta:
        verbose_name = "Compte Bancaire"  # Optional human-readable name for the model
        verbose_name_plural = "Comptes Bancaires"  # Optional human-readable name for multiple instances

        
class PayPalAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # One-to-many relationship
    paypal_email = models.CharField(max_length=255, unique=True)
    paypal_password_hash = models.CharField(max_length=255)

    def set_paypal_password(self, password):
        # Hash the password before saving
        self.paypal_password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.save()

    def check_paypal_password(self, password):
        # Check if provided password matches stored hash
        return bcrypt.checkpw(password.encode('utf-8'), self.paypal_password_hash.encode('utf-8'))
    