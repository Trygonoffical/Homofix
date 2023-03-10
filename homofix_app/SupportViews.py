from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Support,Customer,Product,Booking,CustomUser,Task,Technician,Category,STATE_CHOICES,Rebooking
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
    

    technicians = Technician.objects.all()
    order_count = Booking.objects.filter(status="New").count()

   
    tasks = Task.objects.all()
    
    bookings = Booking.objects.all()
    for i in bookings:
        print(i.product.name)

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
    'tasks':tasks,
    'order_count':order_count
    
    
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
    category = Category.objects.all()
    state_choices = STATE_CHOICES
    supported_by = request.user.support

    if request.method == 'POST':

        customer_id = request.session.get('customer_id')
        product_id = request.POST.getlist('product_id')
        booking_date_str = request.POST.get('booking_date')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        address = request.POST.get('address')
        city = request.POST.get('city')
        area = request.POST.get('area')
        description = request.POST.get('description')
        customer = Customer.objects.get(id=customer_id)
       
        product = Product.objects.filter(id__in=product_id)

        
        booking_date = datetime.strptime(booking_date_str, "%Y-%m-%dT%H:%M")
        
        booking = Booking(customer=customer, booking_date=booking_date,state=state,zip_code=zip_code,address=address,description=description,city=city,area=area, supported_by=supported_by)
        booking.save()
        booking.product.add(*product)
        messages.success(request, 'Booking created successfully.')
        return redirect('support_orders')

    context = {
        'prod': prod,
        'state_choices':state_choices,
        'category':category
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


# def support_Task_assign(request):
    
#     if request.method == "POST":
#         booking_id = request.POST.get('booking_id')
#         technician_id = request.POST.get('technician_id')

#         booking = Booking.objects.get(id=booking_id)
#         technician = Technician.objects.get(id=technician_id)
#         task = Task.objects.create(booking=booking,technician=technician)
#         task.save()
#         booking.status="Assign"
#         technician.status_choice = "Assign"
#         technician.save()
#         # booking.save()
#         messages.success(request,'Assign Task Successfully')
#         return redirect('support_list_of_task')
   


def support_Task_assign(request):
    
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        technician_id = request.POST.get('technician_id')

        booking = get_object_or_404(Booking, id=booking_id)
        technician = get_object_or_404(Technician, id=technician_id)

        task = Task.objects.create(
            booking=booking,
            technician=technician
        )
        task.save()

        booking.status = "Assign"
        booking.save()
        

        technician.status_choice = "Assign"
        technician.save()

        messages.success(request, 'Assign Task Successfully')
        return redirect('support_list_of_task')




def support_List_of_expert(request,id):
    
    booking = Booking.objects.get(id=id)
    
   
    expert = Technician.objects.filter(city=booking.city)
    tasks = Task.objects.filter(booking=booking)
    
    # expert = Technician.objects.filter(city=booking.city, serving_area__icontains=booking.area)
    context = {
        'expert':expert,
        'booking':booking,
        'tasks': tasks,
        
        
        
    }
    
    return render(request,'Support_templates/Orders/list_of_expert.html',context)    

def support_task_counting(request,expert_id):
    technician = Technician.objects.get(id=expert_id)
    print(technician)
    task = Task.objects.filter(id=technician)
    print("tasskkk",task)
    print("gggggggggggg",technician)
    return render(request,'test.html')
    # return redirect('support_List_of_expert',expert_id)

def support_list_of_task(request):
    task = Task.objects.all()
    context = {
        'task':task
    }
    return render(request,'Support_templates/Orders/list_of_task.html',context)    

def order_cancel(request):
    booking = Booking.objects.filter(status="cancelled")
    context = {
        'booking':booking
    }
    return render(request,'Support_templates/Orders/cancel_order.html',context)    

def support_booking_complete(request):
    task = Task.objects.filter(booking__status = "completed")
    context = {
        'task':task
    }
    return render(request,'Support_templates/Rebooking/booking_complete.html',context)    

def support_rebooking(request):
    rebooking = Rebooking.objects.all()
    context = {
        'rebooking' :rebooking
    }
    return render(request,'Support_templates/Rebooking/rebooking.html',context)    
    

def support_rebooking_update(request,id):
    task = Task.objects.get(id=id)

    if request.method == "POST":
        rebooking = Rebooking(booking=task.booking)
        rebooking.save()
        messages.success(request,'Rebooking Successfully')
        return redirect('support_booking_complete')
        # rebooking here
    context = {
        'task':task
    }
    return render(request,'Support_templates/Rebooking/rebooking_update.html',context)    
    

def support_list_of_expert(request):
    category = Category.objects.all()
    technician = Technician.objects.all()
    task = Task.objects.all()
    
    context = {
        'category':category,
        'technician':technician,
        'abcc':task
    }

    return render(request,'Support_templates/Expert/expert.html',context)    


def support_add_expert(request):
    category = Category.objects.all()
    technician = Technician.objects.all()
    if request.method == "POST":
        
        category_id = request.POST.get('category_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       

        ctg = Category.objects.get(id=category_id)
      
        if CustomUser.objects.filter(username = username).exists():
            # return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
            messages.error(request,'Username is already Taken')
            return redirect('support_list_of_expert')
            
        user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type='2')
        user.technician.category = ctg
        user.technician.status = "New"
        user.save()
        messages.success(request,'Expert Register Successfully')
        return redirect('support_list_of_expert')
        # if(user.is_active):
        #     return JsonResponse({'status':'Save'})
            
        # else:
        #     return JsonResponse({'status':0})

    # return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician})



def expert_edit_profile(request,id):
    technician = Technician.objects.get(id=id)
    state_choices = STATE_CHOICES
    # print("ahsssssss",cit)
    category = Category.objects.all()
    # city_choices = [
    #     ('city1', 'City 1'),
    #     ('city2', 'City 2'),
    #     ('city3', 'City 3'),
    # ]
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        email = request.POST.get('email')
        father_name = request.POST.get('father_name')    
        category_id = request.POST.get('category_id')
        mob_no = request.POST.get('mob_no')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        permanent_address = request.POST.get('permanent_address')
        id_proof = request.POST.get('id_proof')
        id_nob = request.FILES.get('id_nob')
        rating = request.POST.get('rating')
        serving_area = request.POST.get('serving_area')
        highest_qualification = request.POST.get('highest_qualification')
        state = request.POST.get('state')
        city = request.POST.get('city')
        status = request.POST.get('status')   
        date_of_joining = request.POST.get('date_of_joining')   
        application_form = request.FILES.get('application_form')   
        

        technician.admin.username = username
        technician.admin.email = email
        if profile_pic != None:
            technician.profile_pic=profile_pic

        technician.Father_name=father_name
        technician.mobile=mob_no
        technician.present_address=present_address
        technician.permanent_address=permanent_address
        technician.Id_Proof=id_proof

        if id_nob != None:
            technician.id_proof_document=id_nob

        if status == 'Deactivate':
            technician.status = "Deactivate"
            
        elif status == 'Hold':
            technician.status = 'Hold'
        else:
            technician.status = 'Active'

        technician.rating=rating
        technician.serving_area=serving_area
        technician.highest_qualification=highest_qualification
        technician.state=state
        technician.city=city
        technician.joining_date=date_of_joining
        if application_form != None:
            technician.application_form=application_form
        

        cat = Category.objects.get(id=category_id)

        technician.category=cat

        technician.admin.save()
        technician.save()
        messages.success(request,'updated sucessfully')
        return redirect('expert_edit_profile',id=technician.id)
        # return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})
        # return redirect('technician_edit_profile',{'technician_id': technician_id})
    return render(request,'Support_templates/Expert/expert_profile.html',{'technician':technician,'category':category,'state_choices':state_choices})

# ------------------------ Testing for session --------------------------- 

def myView(request):
    # Store data in the session
    request.session['my_data'] = 'Hello, World!'
    return HttpResponse('Data stored in the session.')


def another_view(request):
    # Retrieve data from the session
    my_data = request.session.get('my_data', 'Default value if key does not exist')
    return HttpResponse(my_data)
