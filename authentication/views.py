from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def home(request):
    request.session.flush()  # Clear session data
    logout(request)  # Destroy the session
    return render(request, "authentication/index.html")

def base(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    return render(request, "authentication/base.html")

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