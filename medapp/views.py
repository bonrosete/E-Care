from django.shortcuts import render, redirect
from . models import Accounts, Appointment, Account_Info, MedicalHistory, Requests, Test, LoginRecord, Specialization
from django import forms
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.dateparse import parse_date
import dateutil.parser as dparser
from django.db.models import Value
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist
import json
# Create your views here.

def index(request):
	return render(request, 'index.html')


def about(request):
	return render(request, 'about.html')

def news(request):
	return render(request, 'news.html')

def calendar(request):
	return render(request, 'test_calendar.html')


def register(request, methods=['GET', 'POST']):
	if(request.method == 'POST'):
		password = request.POST['password']
		password_check = request.POST['password_check']

		if password == password_check:
			username = request.POST['username']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			birthday = request.POST['birthday']
			address = request.POST['address']
			email = request.POST['email']
			age = request.POST['age']
			gender = request.POST['gender']
			acc_info = Account_Info(
				first_name=first_name,
				last_name=last_name,
				birthday=birthday,
				address=address,
				email=email,
				age=age,
				gender=gender,
				account_type='Patient'
				)
			acc_info.save()
			ref_id = Account_Info.objects.get(first_name=first_name, last_name=last_name)
			acc_login = Accounts(username=username,password=password, reference_id=ref_id.id)
			acc_login.save()
			return redirect('/')
	return render(request, 'register.html')


def login(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password_check = request.POST['password']
		if(Accounts.objects.filter(username=username, password=password_check)):
			request.session['logged_in'] = True
			request.session['username'] = username
			ac = Account_Info.objects.get(id=Accounts.objects.get(username=username, password=password_check).id)
			request.session['account_type'] = ac.account_type
			request.session['login_time'] = timezone.now().strftime('%Y-%m-%dT%H:%M:%S')
			return redirect('/dashboard')
		else:
			return render(request, 'login.html', {'error' : 'Invalid username or password'})
	return render(request, 'login.html')


def logout(request):
	request.session['logout_time'] = timezone.now().strftime('%Y-%m-%dT%H:%M:%S')
	saveLogin = LoginRecord(username=request.session['username'],
				login=request.session['login_time'],
				logout=request.session['logout_time'])
	saveLogin.save()
	request.session.clear()
	return redirect('/')


def dashboard(request):
	if 'logged_in' in request.session:
		user_id = Accounts.objects.get(username=request.session['username'])
		current_user = Account_Info.objects.get(id=user_id.id)
		user_full_name = current_user.first_name + ' ' + current_user.last_name
		datenow = timezone.now().date()
		current_appointments = Appointment.objects.filter(patient=user_full_name, date=datenow)

		# Checks if there is new appointment after the last logout of the user FOR PATIENT ONLY
		if request.session['account_type'] == 'Patient':
			try:
				latest_logout = LoginRecord.objects.filter(username=request.session['username']).latest('logout')
				latest_appointments = Appointment.objects.filter(patient=user_full_name, timestamp__gt=latest_logout.logout)
				context = {'current_appointments': current_appointments,
					'latest_appointments': latest_appointments,
					'notice': 'You have upcoming appointment'}
			except ObjectDoesNotExist:
				context = {'current_appointments': current_appointments,
					'notice': 'You have upcoming appointment'}	
		else:
			context = {'current_appointments': current_appointments,
			'notice': 'You have upcoming appointment'}
		
		return render(request, 'dashboard.html', context)
	else:
		return HttpResponse('Invalid access')


def account(request):
	if 'logged_in' in request.session:
		a = Accounts.objects.get(username=request.session['username'])
		user_info = Account_Info.objects.get(id=a.id)
		context = {'fn': user_info.first_name, 
					'ln': user_info.last_name,
					'birthday': dparser.parse(user_info.birthday),
					'address': user_info.address,
					'email': user_info.email,
					'age': user_info.age,
					'gender': user_info.gender
					}
	return render(request, 'account.html', context)


def makeAppointment(request, methods=['GET', 'POST']):

	if request.method == 'POST':
		doctor_name = request.POST['search']
		all_doctors = Account_Info.objects.filter(account_type='Doctor')
		full_doc_name = all_doctors.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
		doctors = full_doc_name.filter(full_name__icontains=doctor_name)
		doc_spec = Specialization.objects.all()
	else:
		doctors = Account_Info.objects.filter(account_type='Doctor')
	return render(request, 'make_appointment.html', {'doctors':doctors})

	# return render(request, 'make_appointment.html', {'doctors':doctors}, {'specialization': doctor_specialization})

def mySchedule(request):
	if 'logged_in' in request.session:
		user_id = Accounts.objects.get(username=request.session['username'])
		current_user = Account_Info.objects.get(id=user_id.id)
		user_full_name = current_user.first_name + ' ' + current_user.last_name
		sort_appointment = Appointment.objects.order_by('date')
		user_appointment = sort_appointment.filter(patient=user_full_name)
		for ua in user_appointment:
			if ua.date < timezone.now().date():
				print('TRUE')
				print('Moving the appointment to medical history...')
				mh_save = MedicalHistory(diagnosis=ua.purpose,doctor_name=ua.doctor,
					patient_name=ua.patient,date=ua.date)
				mh_save.save()
				Appointment.objects.filter(id=ua.id).delete()
				print(ua.id)
				print('Move successful...')
			else:
				print('FALSE')
		sort_appointment = Appointment.objects.order_by('date')
		user_appointment = sort_appointment.filter(patient=user_full_name)
		requests = Requests.objects.filter(patient=user_full_name)
		context = {'user_appointment': user_appointment, 'requestCount': requests.count()}
	return render(request, 'my_schedule.html', context)


def cancelSchedule(request, id):
	# Cancel the appointment from the patient dashboard
	cancelAppointment = Appointment.objects.get(id=id).delete()
	print('Remove successful')
	return redirect('/dashboard')

# def settings(request):
# 	return render(request, 'settings.html')

# Test for appointment system
def test(request, id):
	# Display name of selected doctor
	doctor_selected = Account_Info.objects.get(id=(id))
	doctor_bd = dparser.parse(doctor_selected.birthday)
	user_id = Accounts.objects.get(username=request.session['username'])
	current_user = Account_Info.objects.get(id=user_id.id)
	# Save to database
	if request.method == 'POST':
		date = request.POST['date']
		time_range = Appointment.objects.filter(doctor='Kim Omar Roxas', date=date)
		startTime = request.POST['timeStart']
		endTime = request.POST['timeEnd']
		purpose = request.POST['purpose']
		parseST = dparser.parse(startTime)
		st = parseST.strftime('%H:%M:%S')
		parseET = dparser.parse(endTime)
		et = parseET.strftime('%H:%M:%S')
		request = Requests(	date=date,
									starttime=st,
									endtime=et,
									doctor=(doctor_selected.first_name + ' ' + doctor_selected.last_name), 
									patient=(current_user.first_name + ' ' + current_user.last_name), 
									purpose=purpose)
		request.save()
		return redirect('/dashboard')
		return render(request, 'test.html',{'doctor_selected': doctor_selected, 'time_range': time_range})
	else:
		return render(request, 'test.html',{'doctor_selected': doctor_selected})

# Validate the date if it has an existing appointment
def validate_date(request):
	date = request.GET.get('date', None)
	# time_range = Appointment.objects.get(date=date)
	# context = {'start_time': time_range.starttime, 'end_time': time_range.endtime}
	# data = json.dumps(context)
	# result = Appointment.objects.get(date=date)
	has_appointment = Appointment.objects.filter(date=date).exists()
	result = Appointment.objects.filter(date=date)
	if has_appointment == True:
		result = Appointment.objects.get(date=date)
		print(result)
		# data = {
		# 'has_appointment': Appointment.objects.get(date=date).exists(),
		# 'time_start': result[0].starttime,
		# 'time_end': result[0].endtime,
		# 'result': result
		# }
		data = {
			'start': result.starttime,
			'end': result.endtime,
		}
		# return render(request, 'test.html', data)
		return JsonResponse(data)
	else:
		# data = {}
		return render(request, 'test.html', {'data': result})

	# return JsonResponse(data)
	# return HttpResponse(data, content_type='application/json')

# JQuery date time picker: DONE, refer to test view
def datetime(request):
	return render(request, 'datetime.html')


def medicalHistory(request):
	user_id = Accounts.objects.get(username=request.session['username'])
	current_user = Account_Info.objects.get(id=user_id.id)
	user_full_name = current_user.first_name + ' ' + current_user.last_name
	sort_history = MedicalHistory.objects.order_by('date')
	medical_history =sort_history.filter(patient_name=user_full_name)
	# medicalHistory = MedicalHistory.objects.filter(patient_name=user_full_name)
	context = {'medical_history': medical_history}
	return render(request, 'medical_history.html', context)


def appointments(request):
	account = Accounts.objects.get(username=request.session['username'])
	doctor = Account_Info.objects.get(id=account.id)
	appointments = Appointment.objects.filter(doctor=doctor.first_name + ' ' + doctor.last_name)
	return render(request, 'appointments.html', {'appointments': appointments})


def removeAppointment(request, id):
	history = Appointment.objects.get(id=id)
	historySave = MedicalHistory(diagnosis=history.purpose, 
								doctor_name=history.doctor, 
								patient_name=history.patient,
								date=history.date)
	historySave.save()
	Appointment.objects.filter(id=id).delete()
	return redirect('/appointments')


def requests(request):
	user_id = Accounts.objects.get(username=request.session['username'])
	current_user = Account_Info.objects.get(id=user_id.id)
	user_full_name = current_user.first_name + ' ' + current_user.last_name
	requests = Requests.objects.filter(doctor=user_full_name)
	context = {'requests': requests}
	return render(request, 'requests.html', context)


def acceptRequest(request, id):
	requestToAccept = Requests.objects.get(id=id)
	acceptRequest = Appointment(purpose=requestToAccept.purpose, 
								doctor=requestToAccept.doctor, 
								patient=requestToAccept.patient,
								date=requestToAccept.date,
								endtime=requestToAccept.endtime,
								starttime=requestToAccept.starttime)
	acceptRequest.save()
	Requests.objects.filter(id=id).delete()
	return redirect('/dashboard')


def modifyRequest(request, id):
	requestToModify = Requests.objects.get(id=id)
	context = {'modify': requestToModify}
	if request.method == 'POST':
		startTime = request.POST['timeStart']
		endTime = request.POST['timeEnd']
		parseST = dparser.parse(startTime)
		st = parseST.strftime('%H:%M:%S')
		parseET = dparser.parse(endTime)
		et = parseET.strftime('%H:%M:%S')
		requestToModify.starttime = st
		requestToModify.endtime = et
		requestToModify.ismodified = 1
		modified_appointment = Appointment(purpose=requestToModify.purpose,doctor=requestToModify.doctor,
			patient=requestToModify.patient,date=requestToModify.date,starttime=st,endtime=et,
			ismodified=1)
		modified_appointment.save()
		Requests.objects.filter(id=id).delete()
		return redirect('/dashboard')
	return render(request, 'modify_request.html', context)


# Comparing time using TimeField
def testTime(request):
	time = Test.objects.get(id=1)
	datenow = timezone.now().time()
	def time_in_range(start, end, now):
		if start <= end:
			return start <= now <= end
		else:
			return start <= now or now <= end
	result = time_in_range(time.starttime, time.endtime, datenow)
	context = {'time': time, 'datenow': datenow, 'result': result}
	return render(request, 'test_time.html', context)

def notifications(request):
	if 'logged_in' in request.session:
		user_id = Accounts.objects.get(username=request.session['username'])
		current_user = Account_Info.objects.get(id=user_id.id)
		user_full_name = current_user.first_name + ' ' + current_user.last_name
		datenow = timezone.now().date()
		current_appointments = Appointment.objects.filter(patient=user_full_name, date=datenow)

		# Checks if there is new appointment after the last logout of the user FOR PATIENT ONLY
		if request.session['account_type'] == 'Patient':
			try:
				latest_logout = LoginRecord.objects.filter(username=request.session['username']).latest('logout')
				latest_appointments = Appointment.objects.filter(patient=user_full_name, timestamp__gt=latest_logout.logout)
				context = {'current_appointments': current_appointments,
					'latest_appointments': latest_appointments,
					'notice': 'You have upcoming appointment'}
			except ObjectDoesNotExist:
				context = {'current_appointments': current_appointments,
					'notice': 'You have upcoming appointment'}	
		else:
			context = {'current_appointments': current_appointments,
			'notice': 'You have upcoming appointment'}
		
		return render(request, 'notifications.html', context)
	else:
		return HttpResponse('Invalid access')



def sample(request, methods=['GET', 'POST']):
	if request.method == 'POST':
		request.session['is_logged_in'] = True
		return redirect('/sample-login')
	return render(request, 'sample.html')

def access(request):
	if 'is_logged_in' in request.session:
		return render(request, 'access.html')
	return HttpResponse('NO LOGIN')













