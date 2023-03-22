from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from .models import Technician,Task,Booking,Rebooking
from django.contrib import messages


@login_required(login_url='/')
def dashboard(request):
    return render(request,'Technician_templates/Dashboard/dashboard.html')



def expert_task_assign(request):
    user = request.user
    

    technician=Technician.objects.get(admin=user)
    task = Task.objects.filter(technician=technician)
    context = {
        'task':task

    }
    
    return render(request,'Technician_templates/Task/task.html',context)



def update_booking_status(request,booking_id):
    task = Booking.objects.get(id=booking_id)
    
    # user = request.user.id
    # tech = Technician.objects.get(admin=user)
    # print("demoooooooooooooooooo",tech)

    # tec = Technician.objects.get(id=request.user.id)
    # print("technician id",tec)
    
    if request.method == 'POST':
        status = request.POST['status']
        
        # print("testingggggggggggg",xyzz.technician.status_choice)
        task.status = status
        task.save()
        messages.success(request, f"Booking status updated to {status}")
        return redirect('expert_task_assign')
   
    
def expert_rebooking_Task(request):
    user = request.user
    

    technician=Technician.objects.get(admin=user)
    rebooking = Rebooking.objects.filter(technician=technician)
    
    context = {
        'rebooking':rebooking

    }
    return render(request,'Technician_templates/Rebooking/rebooking_Details.html',context)   



def update_rebooking_status(request,booking_id):
    print("heloooooo")
    task = Rebooking.objects.get(id=booking_id)
    
    # user = request.user.id
    # tech = Technician.objects.get(admin=user)
    # print("demoooooooooooooooooo",tech)

    # tec = Technician.objects.get(id=request.user.id)
    # print("technician id",tec)
    
    if request.method == 'POST':
        status = request.POST['status']
        
        # print("testingggggggggggg",xyzz.technician.status_choice)
        task.status = status
        task.save()
        messages.success(request, f"Booking status updated to {status}")
        return redirect('expert_task_assign')
 