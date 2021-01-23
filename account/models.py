from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators
from account.validation import Validator

# Create your models here.
class MyProfile(models.Model):
    category = (("male", "Male"), ("female", "Female"), ("other", "Other"))
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    mobile = models.IntegerField(validators=[Validator.mobile])
    gender = models.CharField(max_length=50, choices=category)
    manager = models.CharField(max_length=225, null=True, blank=True)
    profile_pic = models.ImageField(default='none.png', upload_to='profile_pic/', null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)

    @property
    def managers(self):
        pass

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


