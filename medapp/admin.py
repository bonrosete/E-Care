from django.contrib import admin
from . models import Accounts, MedicalHistory, Appointment, Account_Info, Requests

# Register your models here.

admin.site.register(Accounts)
admin.site.register(Account_Info)
admin.site.register(MedicalHistory)
admin.site.register(Appointment)
admin.site.register(Requests)