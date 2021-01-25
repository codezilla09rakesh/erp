from django.db import models
from account.models import CustomUser

# Create your models here.

class YourEmployee(models.Model):
    manager = models.ForeignKey(to=CustomUser, related_name='manager', on_delete=models.CASCADE)
    employee = models.ForeignKey(to=CustomUser, related_name='employee', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.manager.first_name)


class Leave(models.Model):
    day = (('first_half', 'First Half'), ('second_half', 'Second Half'))
    status = (('panding', 'Panding'), ('accepted', 'Accepted'), ('resion', 'resion'))
    manager = models.ForeignKey(to=CustomUser, related_name='leave_manager', on_delete=models.CASCADE)
    employee = models.ForeignKey(to=CustomUser, related_name='leave_employee', on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    description = models.TextField()
    starting_date = models.DateField()
    ending_date = models.DateField()
    half_day = models.CharField(max_length=225, choices=day)
    status = models.CharField(max_length=225, choices=status)
    cr_date = models.DateTimeField(auto_now_add=True)

class Resion(models.Model):
    employee = models.ForeignKey(to=CustomUser, related_name='resion_employee', on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    description = models.TextField()
    cr_date = models.DateTimeField(auto_now_add=True)




