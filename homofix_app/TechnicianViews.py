from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from .models import Technician,Task,Booking
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



def update_booking_status(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    if request.method == 'POST':
        status = request.POST['status']
        booking.status = status
        booking.save()
        messages.success(request, f"Booking status updated to {status}")
        return redirect('expert_task_assign')
    
    # context = {
    #     'booking': booking
    # }
    # return render(request, 'Technician_templates/Task/update_booking_status.html', context)