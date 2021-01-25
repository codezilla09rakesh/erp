from django.contrib import admin
from holiday.models import YourEmployee, Leave

# Register your models here.
admin.site.register(Leave)
admin.site.register(YourEmployee)
