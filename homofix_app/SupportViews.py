from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Support,Customer,Product,Booking,CustomUser,Task,Technician
from datetime import datetime,timedelta
from django.utils import timezone
from django.conf import settings

@login_required(login_url='/')
def dashboard(request):
    return render(request,'Support_templates/Dashboard/dashboard.html')

def support_profile(request):
    return render(request,'Support_templates/Profile/profile.html')



def support_profile_update(request):
    if request.method == "POST":
        support_id = request.POST.get('support_id')
       
        profile_pic = request.FILES.get('profile_pic') 
        username = request.POST.get('username')
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        address = request.POST.get('address')
        status = request.POST.get('status')

        support = Support.objects.get(id=support_id)

       
        support.admin.username =username 
        support.admin.email =email
        if profile_pic != None:
            support.profile_pic =profile_pic
         
        support.address =address 
        support.mobile =mob_no 

        if status == 'Deactivate':
            support.status = "Deactivate"
            
        elif status == 'Hold':
            support.status = 'Hold'
        else:
            support.status = 'Active'

        support.save()
        messages.success(request,'Support Updated Succesffully')
        return HttpResponseRedirect(reverse("support_profile"))

def support_orders(request):
    # booking = Booking.objects.all() 
    technicians = Technician.objects.all()
    tasks = Task.objects.all()
    
    # bookings = Booking.objects.filter(customer=request.user.support).select_related('product', 'supported_by')
    support = request.user.support
    bookings = Booking.objects.filter(supported_by=support)
    if request.method == "POST":
        username = request.POST.get('username')
        mob = request.POST.get('mob')
 
        if Customer.objects.filter(admin__username=username, mobile=mob).exists():
            user= CustomUser.objects.get(username=username)
            request.session['cust_id'] = user.customer.id
            return JsonResponse({'status':'Save'})
        
        else:
            if CustomUser.objects.filter(username=username):
                return JsonResponse({'status':'Error'})
            user = CustomUser.objects.create(username=username, user_type='4')    
            user.set_password(mob)
            user.customer.mobile = mob
            user.save()
            request.session['customer_id'] = user.customer.id
            return JsonResponse({'status':'Save'})

    context = {
    'bookings':bookings,
    'technicians':technicians,
    'tasks':tasks
    
    
   }    
    return render(request, 'Support_templates/Orders/order.html',context)



def support_otp(request):
    if request.method == "POST":
        mob = request.POST.get('mob')
        username = request.POST.get('username')
    

    
   
        if Customer.objects.filter(admin__username=username, mobile=mob).exists():
            user= CustomUser.objects.get(username=username)
            
            request.session['cust_id'] = user.customer.id
            return redirect('support_otp')
        else:
            if CustomUser.objects.filter(username=username):
                messages.error(request, 'Username already exists')
                return redirect('support_orders')
            user = CustomUser.objects.create(username=username, password=mob, user_type='4')    
            user.customer.mobile = mob
            user.save()
            request.session['customer_id'] = user.customer.id
            
            return redirect('support_otp')
    return render(request,'Support_templates/OTP/otp.html')


def support_verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp == '1234':  
            # OTP is correct, redirect to success page
            # return HttpResponse('otp sucess')
            
            return JsonResponse({'status': 'Save', 'message': 'otp is match'})
            # return redirect('support_orders')
        else:
            # OTP is incorrect, show error message and reload the page
            # messages.error(request, 'Invalid OTP. Please try again.')
            
            return JsonResponse({'status': 'error', 'message': 'otp is not valid'})
            # return render(request, 'Support_templates/OTP/otp.html')
    # return render(request, 'Support_templates/Orders/otp_modal.html')


# def support_booking(request):
#     prod = Product.objects.all()
#     supported_by = request.user.support
   
#     if request.method == 'POST':
        
#         customer_id = request.session.get('customer_id')       
        
#         product_id = request.POST.get('product_id')
#         booking_date_str = request.POST.get('booking_date')
#         customer = Customer.objects.get(id=customer_id)
        
#         product = Product.objects.get(id=product_id)
     
#         # create the booking object
#         booking = Booking(customer=customer, product=product,booking_date=datetime.strptime(booking_date_str, "%Y-%m-%dT%H:%M"),supported_by=supported_by)
#         booking.save()
#         messages.success(request, 'Booking created successfully.')
#         return redirect('support_orders')
    
   
#     context = {
#         'prod':prod
#         }
#     return render(request, 'Support_templates/Booking/create_booking.html', context)


def support_booking(request):
    prod = Product.objects.all()
    supported_by = request.user.support

    if request.method == 'POST':

        customer_id = request.session.get('customer_id')
        product_id = request.POST.get('product_id')
        booking_date_str = request.POST.get('booking_date')
        customer = Customer.objects.get(id=customer_id)
        product = Product.objects.get(id=product_id)

        # convert booking date string to datetime object
        # local_tz = pytz.timezone('Asia/Kolkata')  # replace with your local time zone
        booking_date = datetime.strptime(booking_date_str, "%Y-%m-%dT%H:%M")
        # booking_date = local_tz.localize(booking_date)
        # booking_date_utc = booking_date.astimezone(pytz.utc)

        # create the booking object
        booking = Booking(customer=customer, product=product, booking_date=booking_date, supported_by=supported_by)
        booking.save()
        messages.success(request, 'Booking created successfully.')
        return redirect('support_orders')

    context = {
        'prod': prod
    }
    return render(request, 'Support_templates/Booking/create_booking.html', context)

def reschedule_booking(request):
    if request.method == "POST":

        booking_id=request.POST.get('booking_id')
        booking_date=request.POST.get('booking_date')
        booking = Booking.objects.get(id=booking_id)
        booking.booking_date = booking_date
        booking.save()
        messages.success(request,"Your order reschedule success")

        return redirect('support_orders')



def cancel_booking(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking has been cancelled.')
    return redirect('support_orders')    


def support_Task_assign(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        technician_id = request.POST.get('technician_id')

        booking = Booking.objects.get(id=booking_id)
        technician = Technician.objects.get(id=technician_id)
        task = Task.objects.create(booking=booking,technician=technician)
        task.save()
        messages.success(request,'Assign Task Successfully')
        return redirect('support_orders')
    # 
    # print("technician id",tect_id)
    return redirect('support_orders')


def support_list_of_task(request):
    task = Task.objects.all()
    context = {
        'task':task
    }
    return render(request,'Support_templates/Orders/list_of_task.html',context)    
# ------------------------ Testing for session --------------------------- 

def myView(request):
    # Store data in the session
    request.session['my_data'] = 'Hello, World!'
    return HttpResponse('Data stored in the session.')


def another_view(request):
    # Retrieve data from the session
    my_data = request.session.get('my_data', 'Default value if key does not exist')
    return HttpResponse(my_data)
