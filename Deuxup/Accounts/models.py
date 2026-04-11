from django.db import models
from django.contrib.auth.models import AbstractUser
# Lớp User
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"
        SELLER = "seller", "Seller"

    email = models.EmailField(unique=True)    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
            super().save(*args, **kwargs)
            