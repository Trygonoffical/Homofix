from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Support,Customer,Product,Booking,CustomUser,Task,Technician,Category,STATE_CHOICES,Rebooking,BookingProduct,SubCategory,ContactUs,JobEnquiry
# from datetime import datetime,timedelta
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
from django.http import Http404
import random
import datetime
import requests
import urllib.parse





@login_required(login_url='/')
def dashboard(request):
    user = request.user
    support = Support.objects.get(admin=user)  
    context = {
        
        'support':support
    }

    return render(request,'Support_templates/Dashboard/dashboard.html',context)

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


# def support_orders(request):
    
#     technicians = Technician.objects.all()
#     order_count = Booking.objects.filter(status="New").count()
#     user = request.user
#     support = Support.objects.get(admin=user)
    


#     # i want calcualate here 
#     tasks = Task.objects.all()   
#     bookings = Booking.objects.filter(status="New")
    
#     total_price = 0
   
    


#     if request.method == "POST":
       
#         random_number = random.randint(0, 999)
#         unique_number = str(random_number).zfill(3)
       
        
#         # username = request.POST.get('username')
#         first_name = request.POST.get('full_name')
        
#         mob = request.POST.get('mob')

#         cus = Customer.objects.filter(admin__first_name=first_name)
        
 
#         if Customer.objects.filter(admin__first_name=first_name, mobile=mob).exists():
           
#             user= CustomUser.objects.get(first_name=first_name)
#             request.session['cust_id'] = user.customer.id
#             return JsonResponse({'status':'Save'})
        
#         else:
#             # print
#         #     if CustomUser.objects.filter(username=first_name):
#         #         return JsonResponse({'status':'Error'})
#             user = CustomUser.objects.create(username=first_name+unique_number,first_name=first_name, user_type='4')    
#             user.set_password(mob)
#             user.customer.mobile = mob
#             user.save()
#             request.session['customer_id'] = user.customer.id
#             return JsonResponse({'status':'Save'})

#     context = {
#     'bookings':bookings,
#     'technicians':technicians,
#     'tasks':tasks,
#     'order_count':order_count,
#     'total_price':total_price,
#     'support':support
    
    
#    }    
#     return render(request, 'Support_templates/Orders/order.html',context)


def support_orders(request):
    
    technicians = Technician.objects.all()
    order_count = Booking.objects.filter(status="New").count()
    user = request.user
    support = Support.objects.get(admin=user)
    


    # i want calcualate here 
    tasks = Task.objects.all()   
    bookings = Booking.objects.filter(status="New")
    
    total_price = 0
   
    


    if request.method == "POST":
        # print("testing")
        otp_number = random.randint(0,9999)
        otp_unique = str(otp_number).zfill(3)
       
        first_name = request.POST.get('full_name')      
        mob = request.POST.get('mob')


        request.session['full_name'] = first_name
        request.session['mob'] = mob
        request.session['otp'] = otp_unique


        auth_key = "IQkJfqxEfD5l3qCu"
        sender_id = "TRYGON"
        route = 2
        number = mob
        # message = f"Dear {first_name} {otp_unique} is the OTP for your verify mobile number . In case you have not requested this, please contact us at info@trygon.in"
        message = f"Dear {first_name} {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
        print("messageeeeeeee",message)
        # message = "Dear armuu 1005 is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
        template_id = "1707162192151162124"
        url = f"http://weberleads.in/http-tokenkeyapi.php?authentic-key={auth_key}&senderid={sender_id}&route={route}&number={number}&message={urllib.parse.quote(message)}&templateid={template_id}"
        response = requests.get(url) 
                
        # if response.ok:
        #     print("SMS message sent successfully")
            
        # else:
        #     print("Error sending SMS message")
        return JsonResponse({'status':'Save'})
       
        
       
        
        # username = request.POST.get('username')
       
        # cus = Customer.objects.filter(admin__first_name=first_name)
        
 
        
        

    context = {
    'bookings':bookings,
    'technicians':technicians,
    'tasks':tasks,
    'order_count':order_count,
    'total_price':total_price,
    'support':support
    
    
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
        otp_num = request.session.get('otp', 'Default value if key does not exist')
        
        

        otp = request.POST.get('otp')
        if otp == otp_num:  
            # OTP is correct, redirect to success page
            # return HttpResponse('otp sucess')
            
            random_number = random.randint(0, 999)
            unique_number = str(random_number).zfill(3)
       
            first_name = request.session.get('full_name', 'Default value if key does not exist')
            mob = request.session.get('mob', 'Default value if key does not exist')
            user = CustomUser.objects.create(username=first_name+unique_number,first_name=first_name, user_type='4')    
            user.set_password(mob)
            user.customer.mobile = mob
            user.save()
            request.session['customer_id'] = user.customer.id

            return JsonResponse({'status': 'Save', 'message': 'otp is match'})
            # return redirect('support_orders')
        else:
            # OTP is incorrect, show error message and reload the page
            # messages.error(request, 'Invalid OTP. Please try again.')
            
            return JsonResponse({'status': 'error', 'message': 'otp is not eeee valid'})
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
    user = request.user
    support = Support.objects.get(admin=user)
    prod = Product.objects.all()
    category = Category.objects.all()
    state_choices = STATE_CHOICES
    supported_by = request.user.support
    

    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        
        booking_date_str = request.POST.get('booking_date')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        address = request.POST.get('address')
        city = request.POST.get('city')
        area = request.POST.get('area')
        description = request.POST.get('description')
        total_amount = int(request.POST.get('total_amount'))
        
        customer = Customer.objects.get(id=customer_id)
        booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        
        if city:
            city = city.lower()
        booking = Booking.objects.create(
            customer=customer,
            booking_date=booking_date,
            state=state,
            zip_code=zip_code,
            address=address,
            description=description,
            city=city,
            area=area,
            supported_by=supported_by
        )

        for i, product_id in enumerate(product_ids):
            product = Product.objects.get(id=product_id)
            quantity = int(quantities[i])
            price = int(request.POST.getlist('price')[i])
            
            BookingProduct.objects.create(
                booking=booking,
                product=product,
                quantity=quantity,
                total_price=total_amount
                # price=price
            )
            # total_price = sum(price_list)
            # booking.total_price = total_price
            booking.save()

        messages.success(request, 'Booking created successfully.')
        return redirect('support_orders')

    context = {
        'prod': prod,
        'state_choices':state_choices,
        'category':category,
        'support':support
    }
    return render(request, 'Support_templates/Booking/create_booking.html', context)

def reschedule_booking(request):
    if request.method == "POST":

        booking_id=request.POST.get('booking_id')
        booking_date_str = request.POST.get('booking_date')
        booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        print("booking date",booking_date)
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
    user = request.user
    support = Support.objects.get(admin=user)
    
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        technician_id = request.POST.get('technician_id')

        booking = get_object_or_404(Booking, id=booking_id)
        technician = get_object_or_404(Technician, id=technician_id)
        supported_by = request.user.support
        task = Task.objects.create(
            booking=booking,
            technician=technician,
            supported_by=supported_by
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
    user = request.user
    support = Support.objects.get(admin=user)
    order_count = Booking.objects.filter(status="New").count()
    task = Task.objects.all()
    context = {
        'task':task,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Orders/list_of_task.html',context)    

def order_cancel(request):
    user = request.user
    support = Support.objects.get(admin=user)
    order_count = Booking.objects.filter(status="New").count()
    booking = Booking.objects.filter(status="cancelled")
    context = {
        'booking':booking,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Orders/cancel_order.html',context)    

def support_booking_complete(request):
    user = request.user
    support = Support.objects.get(admin=user)  
    order_count = Booking.objects.filter(status="New").count()
    task = Task.objects.filter(booking__status = "completed")
    context = {
        'task':task,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Rebooking/booking_complete.html',context)    
    

# def support_rebooking(request,task_id):
#     task = get_object_or_404(Task, id=task_id)
#     booking_id = task.booking.id
#     booking_prod = BookingProduct.objects.filter(booking_id=booking_id)
#     context = {
#         'booking_prod':booking_prod
#     }
#     # print(booking_prod)
#     return render(request,'Support_templates/Rebooking/rebooking.html',context) 

# def support_rebooking(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     booking_id = task.booking.id
#     booking_prod = BookingProduct.objects.filter(booking_id=booking_id)
    
#     context = {
#         'booking_prod': booking_prod,
        
#     }
#     return render(request, 'Support_templates/Rebooking/rebooking.html', context)


def support_rebooking(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    booking_id = task.booking.id
    user = request.user
    support = Support.objects.get(admin=user)
    
    booking_products = BookingProduct.objects.filter(booking_id=booking_id).select_related('booking', 'product')
    
    for booking_product in booking_products:
        rebookings = Rebooking.objects.filter(booking_product_id=booking_product.id).order_by('-id')
        booking_product.rebookings.set(rebookings)

    context = {
        'booking_prod': booking_products,
        'support':support
        
    }
    return render(request, 'Support_templates/Rebooking/rebooking.html', context)

def support_rebooking_list(request):
    user = request.user
    support = Support.objects.get(admin=user)  
    order_count = Booking.objects.filter(status="New").count()
    rebooking = Rebooking.objects.all()
    context = {
        'rebooking' :rebooking,
        'support':support,
        'order_count':order_count,
        
    }
    return render(request,'Support_templates/Rebooking/rebooking_list.html',context)    



def support_rebooking_update(request):
    if request.method == 'POST':
        booking_product_id = request.POST.get('booking_prod_id')
        
        booking_date = request.POST.get('booking_date')
        
        try:
            # booking_product = BookingProduct.objects.get(booking_id=booking_product_id)
            booking_product = BookingProduct.objects.filter(booking=booking_product_id).first()
            booking = booking_product.booking
            task = Task.objects.get(booking=booking)
        except (BookingProduct.DoesNotExist, Task.DoesNotExist):
            raise Http404('BookingProduct or Task matching query does not exist.')
        
        # create a new rebooking object with the same booking and assign it to the same technician
        rebooking = Rebooking.objects.create(
            booking_product=booking_product,
            technician=task.technician,
            booking_date=booking_date
        )
        
        # update the status of the original booking to "completed"
        task.booking.status = "completed"
        task.booking.save()
        
        rebooking.save()
        print("successsss",rebooking)
        messages.success(request, 'Rebooking successfully created.')
        return redirect('support_booking_complete')

    context = {}
    return render(request, 'Support_templates/Rebooking/booking_complete.html', context)



def support_get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(Category_id=category_id)
    data = list(subcategories.values('id', 'name'))
    return JsonResponse(data, safe=False)

def support_get_products(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        subcategory_id = int(subcategory_id)
        products = Product.objects.filter(subcategory_id=subcategory_id)
        data = [{'id': product.id,'price': product.price, 'name': product.name} for product in products]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)

# def support_rebooking_update(request):
#     if request.method == 'POST':
#         id = request.POST.get('booking_prod_id')
#         try:
#             task = Task.objects.get(booking__id=id)
#         except Task.DoesNotExist:
#             raise Http404('Task matching query does not exist.')
        
#         # create a new rebooking object with the same booking and assign it to the same technician
#         rebooking = Rebooking.objects.create(
#             booking=task.booking,
#             technician=task.technician,
#             booking_date=request.POST.get('booking_date')
#         )
#         rebooking.save()
        
#         # update the status of the original booking to "completed"
#         task.booking.status = "completed"
#         task.booking.save()
        
#         messages.success(request, 'Rebooking successfully created.')
#         return redirect('support_booking_complete')

#     context = {}
#     return render(request, 'Support_templates/Rebooking/booking_complete.html', context)


def support_rebooking_product(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    booking_id = task.booking.id
    booking_prod = BookingProduct.objects.filter(booking_id=booking_id)
    print(booking_prod)
    return render(request, 'Support_templates/Rebooking/rebooking_product.html', {'booking_prod': booking_prod})


    # return render(request,'Support_templates/Rebooking/rebooking_product.html',{'booking_prod':booking_prod})    
def support_expert_add(request):
    
    category = Category.objects.all()
    user = request.user
    support = Support.objects.get(admin=user) 
    order_count = Booking.objects.filter(status="New").count()
    if request.method == "POST":
        current_user = request.user
        
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        sub_category_id = request.POST.getlist('sub_category_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        subcat = SubCategory.objects.filter(id__in=sub_category_id)
        # category_id = request.POST.get('category_id')
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       

        # ctg = Category.objects.get(id=category_id)
      
        # if CustomUser.objects.filter(username = username).exists():
        #     # return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
        #     messages.error(request,'Username is already Taken')
        #     return redirect('support_list_of_expert')
        supported_by = request.user.support 
        user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=first_name+unique_number,password=password,email=email,user_type='2')
        user.technician.subcategories.set(subcat)
        user.technician.status = "New"
        user.technician.supported_by = supported_by
        user.save()
        messages.success(request,'Expert Register Successfully')
        return redirect('support_list_of_expert')

    context = {
        'category':category,
        'support':support,
        'order_count':order_count,
    }
    return render(request,'Support_templates/Expert/add_expert.html',context)
def support_list_of_expert(request):
    user = request.user
    support = Support.objects.get(admin=user)  

    category = Category.objects.all()
    technician = Technician.objects.all()
    task = Task.objects.all()
    order_count = Booking.objects.filter(status="New").count()
    
    context = {
        'category':category,
        'technician':technician,
        'abcc':task,
        'support':support,
        'order_count':order_count,
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
    user = request.user
    support = Support.objects.get(admin=user) 
    technician = Technician.objects.get(id=id)
    order_count = Booking.objects.filter(status="New").count()
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
        # category_id = request.POST.get('category_id')
        subcategory_id = request.POST.getlist('sub_category_id')
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
        

        # cat = Category.objects.get(id=category_id)
        if subcategory_id:
            subcategories = SubCategory.objects.filter(id__in=subcategory_id)
            technician.subcategories.set(subcategories)
           

        # technician.category=cat

        technician.admin.save()
        technician.save()
        messages.success(request,'updated sucessfully')
        return redirect('expert_edit_profile',id=technician.id)
        # return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})
        # return redirect('technician_edit_profile',{'technician_id': technician_id})
    return render(request,'Support_templates/Expert/expert_profile.html',{'technician':technician,'category':category,'state_choices':state_choices,'support':support,'order_count':order_count,})




# ---------------------------- Invoice ------------------------------- 
def invoice(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    context = {
        'booking':booking
    }
    return render(request,'Support_templates/Invoice/invoice.html',context)


# -------------------------------- Contact Us -------------------------- 




def support_contact_us(request):
    user = request.user
    support = Support.objects.get(admin=user)   
    contact_us = ContactUs.objects.all()
    context = {
        'contact_us':contact_us,
        'support':support
    }

    return render(request,'Support_templates/ContactUs/contact_us.html',context)    

def support_job_enquiry(request):
    job_enquiry = JobEnquiry.objects.all()
    context = {
        'job_enquiry':job_enquiry
    }

    return render(request,'Support_templates/JobEnquiry/job_enquiry.html',context)

# ------------------------ Testing for session --------------------------- 

def myView(request):
    # Store data in the session
    request.session['my_data'] = 'Hello, World!'
    return HttpResponse('Data stored in the session.')


def another_view(request):
    # Retrieve data from the session
    my_data = request.session.get('my_data', 'Default value if key does not exist')
    return HttpResponse(my_data)
