from django.contrib import admin
from . models import Accounts, MedicalHistory, Appointment, Account_Info, Requests, Test, Specialization, LoginRecord

# Register your models here.

admin.site.register(Accounts)
admin.site.register(Account_Info)
admin.site.register(MedicalHistory)
admin.site.register(Appointment)
admin.site.register(Requests)
admin.site.register(Test)
admin.site.register(LoginRecord)
admin.site.register(Specialization)
