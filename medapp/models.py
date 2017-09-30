from django.db import models
# Create your models here.


class Accounts(models.Model):
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=45)
	reference = models.ForeignKey('Account_Info',on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now=True)
	latest_logout = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.username


class Account_Info(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	birthday = models.CharField(max_length=45)
	address = models.CharField(max_length=45)
	email = models.CharField(max_length=45)
	age = models.IntegerField()
	genders = (
			('Male', 'Male'),
			('Male', 'Female'),
		)
	gender = models.CharField(max_length=6, choices=genders)
	type = (
			('Patient', 'Patient'),
			('Doctor', 'Doctor'),
		)
	account_type = models.CharField(max_length=10, choices=type)
	timestamp = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.first_name


class MedicalHistory(models.Model):
	diagnosis = models.CharField(max_length=100)
	doctor_name = models.CharField(max_length=100)
	patient_name = models.CharField(max_length=100)
	date = models.DateField(max_length=10)
	timestamp = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.patient_name


class Appointment(models.Model):
	purpose = models.CharField(max_length=100)
	doctor = models.CharField(max_length=50)
	patient = models.CharField(max_length=50)
	date = models.DateField(max_length=50)
	starttime = models.TimeField(max_length=10)
	endtime = models.TimeField(max_length=10)
	timestamp = models.DateTimeField(auto_now=True)
	ismodified = models.BooleanField(default=0)

	def __str__(self):
		return self.doctor


class Requests(models.Model):
	purpose = models.CharField(max_length=100)
	doctor = models.CharField(max_length=50)
	patient = models.CharField(max_length=50)
	date = models.DateField(max_length=50)
	starttime = models.TimeField(max_length=10)
	endtime = models.TimeField(max_length=10)
	timestamp = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.doctor
