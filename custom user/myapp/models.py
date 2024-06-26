from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


ROLE = [
    ('ADMIN', 'Admin'),
    ('STAFF', 'Staff'),
    ('STUDENT', 'Student'),
]


class User(AbstractUser):
    mobile_number = models.CharField(max_length=13, null=False, unique=True)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE)
    

    USERNAME_FIELD = "mobile_number"

    REQUIRED_FIELDS = ["username"]



# class UserManager(BaseUserManager):

#     def create_user(self, mobile_number, password, address):
#         if not mobile_number:
#             raise ValueError("Mobile number is required.")
#         user = self.model(mobile_number=mobile_number, address=address)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, mobile_number, password, address):
#         user = self.create_user(mobile_number, password, address)
#         user.is_active = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

# class User(AbstractUser):
#     mobile_number = models.CharField(max_length=13, null=False, unique=True)
#     address = models.CharField(max_length=255)

#     USERNAME_FIELD = "mobile_number"

#     REQUIRED_FIELDS = ["address"]

#     objects = UserManager()
