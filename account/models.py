from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core import validators
import os
from account.validation import Validator

# Create your models here.
class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    # is_employee = models.BooleanField(default=True)

class MyProfile(models.Model):
    category = (("male", "Male"), ("female", "Female"), ("other", "Other"))
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, validators=[Validator.mobile])
    gender = models.CharField(max_length=50, choices=category)
    profile_pic = models.ImageField(default='static/img/none.png', upload_to='profile_pic/', null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return str(self.user.first_name)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     print("in side a signle ##############################################")
#     if created:
#         if instance.is_superuser:
#             pass
#         else:
#             MyProfile.objects.create(user=instance)
#             print("Profile created")
#
# @receiver(post_save,sender=User)
# def save_user_profile(instance, created, **kwargs):
#     if instance.is_superuser:
#         pass
#     else:
#         instance.myprofile.save()

#

