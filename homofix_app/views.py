from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib import messages

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect('admin_dashboard')

        elif user is not None and user.technician.status == 'Active':
            auth_login(request, user)
            return HttpResponse("Hello, Technician")

        elif user is not None:
            messages.error(request, "Your account is not active.")
            return redirect('login')
        else:
            return HttpResponse("wrong user")
            
            # messages.error(request,"Invalid Login Or Password!!")
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    return render(request,'homofix_app/Authentication/login.html')

def logout_user(request):
    logout(request)
    return redirect("login")
