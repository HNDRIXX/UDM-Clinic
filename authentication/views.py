from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
# from .models import Person
from .models import ConsultData, Employee

# Create your views here.
def home(request):
    request.session.flush()  # Clear session data
    logout(request)  # Destroy the session
    return render(request, "authentication/index.html")

def base(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, "authentication/base.html")

def profile(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, "authentication/profile.html")

def employee(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        empName = request.POST.get('empName')
        empRole = request.POST.get('empRole')

        # Perform form validation
        if not empName or not empRole:
            messages.error(request, 'Please fill in all the fields.')
        else:
            employeeNew = Employee(empName=empName, empRole=empRole)
            employeeNew.save()
            messages.success(request, 'Data saved successfully.')
            return redirect('employee')  # Redirect to the same URL to prevent form resubmission

    employee_data = Employee.objects.all()
    return render(request, 'authentication/employee.html', {'employee_data': employee_data})

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
    
    employee_data = Employee.objects.all()
    consult_data = ConsultData.objects.all()
    return render(request, 'authentication/consultation.html', {'consult_data': consult_data, 'employee_data': employee_data})


def create_person(request):
    # if request.method == 'POST':
    #     print("View function called!")  # Add this line for debugging
    #     name = request.POST.get('name')
    #     age = request.POST.get('age')
    #     person = Person(name=name, age=age)
    #     person.save()
    #     return render(request, 'authentication/success.html')
    
    return render(request, "authentication/consultation.html")

def insert_consult(request):
    
    
    return render(request, "authentication/consultation.html")

def consulted(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    
    consult_data = ConsultData.objects.all()
    return render(request, 'authentication/consulted.html', {'consult_data': consult_data})


def tracklogs(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, "authentication/tracklogs.html")

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
            login(request, user)
            
            return redirect('base')
        
        else:
            messages.error(request, "Wrong Credentials")
            return redirect('home')
            
        
    # return render(request, "authentication/signin.html")

def signout(request):
    pass