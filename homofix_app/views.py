from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,logout, login as auth_login

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect('admin_dashboard')
        elif user is not None:
            auth_login(request, user)
            return HttpResponse("hello user")
        else:
            return HttpResponse("wrong user")
            # messages.error(request,"Invalid Login Or Password!!")
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    return render(request,'homofix_app/Authentication/login.html')

def logout_user(request):
    logout(request)
    return redirect("login")
