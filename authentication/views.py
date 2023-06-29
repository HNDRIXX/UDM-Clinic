from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import Extract
from django.template.defaultfilters import json_script
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
# from .models import Person
from .models import ConsultData, Employee, Illness

import json

# Create your views here.
def get_employee_data(): # Define function for Employee data
    employee_data = Employee.objects.all()
    return employee_data

def get_consultation_data(): # Define function for Consultation data
    consultation_data = ConsultData.objects.all()
    return consultation_data

def get_illness_data(): # Define function for Consultation data
    illness_data = Illness.objects.all()
    return illness_data

def test(request):
    return render(request, "authentication/test.html")

def home(request):
    request.session.flush()  # Clear session data
    logout(request)  # Destroy the session
    return render(request, "authentication/index.html")

def base(request):
    if not request.user.is_authenticated:
        return redirect('home')

    consult_data = ConsultData.objects.all()

    # Get the distinct years from the dateConsult field
    years = set(employee.dateConsult.year for employee in consult_data)

    # Initialize empty dictionaries for each year and patient role
    data = {year: {} for year in years}

    # Count the occurrences of each patient role for each year
    for employee in consult_data:
        year = employee.dateConsult.year
        patient_role = employee.patientRole
        if patient_role not in data[year]:
            data[year][patient_role] = 0
        data[year][patient_role] += 1

    # Prepare the data for Chart.js
    labels = [str(year) for year in years]
    datasets = []

     # Define custom colors for each patient role
    colors = ['#FB756D', '#6DF0FB', '#6D94FB']

    # Create a dataset for each patient role
    for i, patient_role in enumerate(['Student', 'Faculty', 'School Staff']):
        data_points = [data[year].get(patient_role, 0) for year in years]
        dataset = {
            'label': patient_role,
            'data': data_points,
            'backgroundColor': colors[i],
        }
        datasets.append(dataset)

    # for i, patient_role in enumerate(['Student', 'Faculty', 'School Staff', 'OJT']):
    #     data_points = [data[year].get(patient_role, 0) for year in years]
    #     dataset = {
    #         'label': patient_role,
    #         'data': data_points,
    #         'backgroundColor': colors[i],
    #     }
    #     datasets.append(dataset)

    print(labels)
    context = {
        'labels': labels,
        'datasets': datasets,
        'data': json.dumps(data),
        'employee_data': get_employee_data(),
        'consultation_count': get_consultation_data().count(),
        'consulted_count': get_consultation_data().count(),
        'illness_count': get_illness_data().count(),
        'employee_count': get_employee_data().count()
    }

    return render(request, 'authentication/base.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    user = request.user
    passEmpData = {}

    for employee in get_employee_data():
        if employee.empID == user.id:
            passEmpData['empName'] = employee.empName
            passEmpData['empRole'] = employee.empRole
            break

    context = {
        'employee_data': get_employee_data(),
        'passEmpData': passEmpData
    }

    return render(request, 'authentication/profile.html', context)

def employee(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        empName = request.POST.get('empName')
        empRole = request.POST.get('empRole')
        username = request.POST.get('username')
        empPhoneNum = request.POST.get('empPhoneNum')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Perform form validation
        if not empName or not empRole or not username or not empPhoneNum or not password or not email:
            messages.error(request, 'Please fill in all the fields.')
        else:
            employeeNew = Employee(empName=empName, empRole=empRole, empPhoneNum=empPhoneNum)
            employeeNew.save()

            myuser = User.objects.create_user(username, email, password)
            myuser.empName = empName
            myuser.save()

            messages.success(request, 'Data saved successfully.')
            return redirect('employee')

    return render(request, 'authentication/employee.html', {'employee_data': get_employee_data()})

# Define function for Consultation Edit
def consultation_edit(request, consult_id):
    if request.method == 'POST':
        illness = request.POST.get('illness')
        consult_record = ConsultData.objects.get(pk=consult_id)
        consult_record.illness = illness
        consult_record.save()
        messages.success(request, 'Edit succesfully!')
        return redirect('consultation') 

def consultation(request):
    if not request.user.is_authenticated:
        return redirect('home')
    

    if request.method == 'POST':
        print("View function called!")  # Add this line for debugging
        patientName = request.POST.get('patientName')
        patientRole = request.POST.get('patientRole')
        assistName = request.POST.get('assistName')
        dateConsult = request.POST.get('dateConsult')

         # Perform form validation
        if not patientName or not assistName or not dateConsult:
            messages.error(request, 'Please fill in all the fields.')
        else:
            consultRecords = ConsultData(patientName=patientName, patientRole=patientRole, assistName=assistName, dateConsult=dateConsult)
            consultRecords.save()
            messages.success(request, 'New Consult saved successfully.')
            return redirect('consultation')
    consult_data = ConsultData.objects.all()
    illness_data = Illness.objects.all()
    return render(request, 'authentication/consultation.html', {'consult_data': consult_data, 'employee_data': get_employee_data(), 'illness_data': illness_data})

def consulted(request):
    if not request.user.is_authenticated: return redirect('home')
    
    consult_data = ConsultData.objects.all()
    return render(request, 'authentication/consulted.html', {'consult_data': consult_data, 'employee_data': get_employee_data()})

def illness(request):
    if not request.user.is_authenticated: return redirect('home')
    
    if request.method == 'POST':
        illnessName = request.POST.get('illnessName')
        illnessDesc = request.POST.get('illnessDesc')

         # Perform form validation
        if not illnessName or not illnessDesc:
            messages.error(request, 'Please fill in all the fields.')
        else:
            illnessRecords = Illness(illnessName=illnessName, illnessDesc=illnessDesc)
            illnessRecords.save()
            messages.success(request, 'New Illness saved successfully.')
            return redirect('illness')
        
    illness_data = Illness.objects.all()
    return render(request, 'authentication/illness.html', {'illness_data': illness_data, 'employee_data': get_employee_data})

def tracklogs(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, "authentication/tracklogs.html", {'employee_data': get_employee_data()})

def signup(request):

    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(username, email, password)
        myuser.name = name

        myuser.save()
        messages.success(request, 'Account is SUCCESSFULLY REGISTERED!')

        return redirect('base')

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == "POST":        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            # Compare user.id with another table
            employee_obj = Employee.objects.filter(empID=user.id).first()

            # Compare user.id with another table
            # try:
            #     some_model_instance = Employee.objects.get(empID=user.id)
            #     firstName = some_model_instance.empName
            #     login(request, user)
            #     return render(request, 'authentication/base.html', {'firstName': firstName})
            # except Employee.DoesNotExist:
            #     return redirect('home')
        
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('home')
            
        
    # return render(request, "authentication/signin.html")

def signout(request):
    pass