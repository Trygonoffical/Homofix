from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,logout, login as auth_login
from django.contrib import messages

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.user_type == "1":
                auth_login(request, user)
                return redirect('admin_dashboard')
            elif user.user_type == "2" and user.technician.status == 'Active':
                if not request.user.is_authenticated:
                    auth_login(request, user)
                
                return redirect("technician_dashboard")
            elif user.user_type == "3" and user.support.status == 'Active':
                if not request.user.is_authenticated:
                    auth_login(request, user)
                return redirect("support_dashboard")
            elif user.user_type == "4":
                if not request.user.is_authenticated:
                    auth_login(request, user)
                return HttpResponse("Hello, Customer")
            else:
                
                messages.error(request, "Your account is not active.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    if request.user.is_authenticated:
        if request.user.user_type == "1":
            return redirect('admin_dashboard')
        elif request.user.user_type == "2":
            if request.user.technician.status == 'Active':
                return redirect('technician_dashboard')
        
        elif request.user.user_type == "3":
            if request.user.support.status == 'Active':
                return redirect("support_dashboard")
        else:
            return HttpResponse('Customer Dashboard')

    return render(request, 'homofix_app/Authentication/login.html')

def logout_user(request):
    logout(request)
    return redirect("login")
