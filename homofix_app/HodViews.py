from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import CustomUser,Category,Technician,Product,SpareParts,Support,FAQ,Booking,Task,STATE_CHOICES,SubCategory,Rebooking,ContactUs,JobEnquiry,HodSharePercentage,Customer,Share,Payment,Addon,Wallet,WalletHistory,TechnicianLocation,AdminHOD,AllTechnicianLocation,BookingProduct,WithdrawRequest,RechargeHistory,Attendance,Coupon,Kyc,Blog
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import random
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.utils import timezone
from urllib.parse import urlencode
import datetime
from django.http import Http404
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT,TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph,Image
from django.conf import settings
from decimal import Decimal
# def all_location(request):
#     all_location = AllTechnicianLocation.objects.all()
   
#     context = {
#         'technician':all_location
#     }
   
   
#     return render(request, 'all_loaction.html', context)

def all_location(request):
    all_locations = AllTechnicianLocation.objects.all()

    # Create a list of markers for each technician location
    markers = []
    for location in all_locations:
        marker = f"markers=color:red%7C{location.latitude},{location.longitude}"
        markers.append(marker)

    # Combine the markers into a single string
    markers_str = '&'.join(markers)

    # Generate the Google Map iframe URL with the markers
    map_url = f"https://www.google.com/maps/embed/v1/view?key=YOUR_API_KEY_HERE&center={all_locations[0].latitude},{all_locations[0].longitude}&zoom=10&{markers_str}"

    context = {
        'map_url': map_url
    }

    return render(request, 'all_location.html', context)


    # return render(request,'all_loaction.html')
# @login_required
def admin_dashboard(request):
   
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    return render(request,'homofix_app/AdminDashboard/dashboard.html',{'booking_count':booking_count,'new_expert_count':new_expert_count,'rebooking_count':rebooking_count,'customer_count':customer_count})


def admin_profile(request):
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'customer_count':customer_count,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
    }
    return render(request,'homofix_app/AdminDashboard/profile.html',context)


def add_admin(request):
    if request.method == "POST":
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        print("email",email)
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        print(first_name,last_name,email,mobile,password)
        # if AdminHOD.objects.filter(mobile = mobile,admin__email=email).exists():
        #     return JsonResponse({'status': 'error', 'message': 'Mobile Number is already Taken'})
          
        # if AdminHOD.objects.filter(Q(mobile=mobile) | Q(admin__email=email)).exists():
        #     if AdminHOD.objects.filter(mobile=mobile).exists():
        #         return JsonResponse({'status': 'error', 'message': 'Mobile Number is already taken'})
        #     else:
        #         return JsonResponse({'status': 'error', 'message': 'Email is already taken'})
        if AdminHOD.objects.filter(Q(mobile=mobile) | Q(admin__email=email)).exists():
            if AdminHOD.objects.filter(mobile=mobile, admin__email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Mobile Number and Email are already taken'})
            elif AdminHOD.objects.filter(mobile=mobile).exists():
                return JsonResponse({'status': 'error', 'message': 'Mobile Number is already taken'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Email is already taken'})

        user = CustomUser.objects.create(first_name=first_name,last_name=last_name,username=first_name+unique_number,email=email,user_type='1')
        user.set_password(password)
        user.adminhod.mobile = mobile
        user.save()
        return JsonResponse({'status':'Save'})
    # else:
    #     return JsonResponse({'status':'error'})

        
    return render(request,'homofix_app/AdminDashboard/Admin/create_admin.html')

def edit_admin(request,id):
    hod = AdminHOD.objects.get(admin_id=id)
    
    
    
    context = {
        'hod':hod
    }
       
        
        # first_name = request.POST.get('first_name')
        

    return render(request,'homofix_app/AdminDashboard/Admin/edit_admin.html',context)
def update_admin(request):

    if request.method == "POST":  
        print("helloo posting")

        hod_id = request.POST.get('hod_id')
        print("hodddid",hod_id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        hod = CustomUser.objects.get(id=hod_id)
        hod.first_name = first_name
        hod.last_name = last_name
        hod.email = email
        hod.adminhod.mobile = mobile
        print("testinggg",first_name,last_name,email,mobile)
        hod.save()
        messages.success(request,'Admin updated successfully')
        return redirect('admin_list')

def admin_list(request):
    hod = AdminHOD.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'hod':hod,
        'new_expert_count':new_expert_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }
    return render(request,'homofix_app/AdminDashboard/Admin/list_of_admin.html',context)
def admin_update_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # if CustomUser.objects.filter(username = username).exists():
        #     return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
          
        id = request.user.id
        user = CustomUser.objects.get(id=id)
        # user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        print("success")
        return JsonResponse({'status':'Save'})
    else:
        print("erorrrrr")
        
    return render(request,'homofix_app/AdminDashboard/profile.html')

def category(request):
    category = Category.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    return render(request,'homofix_app/AdminDashboard/Category/category.html',{'category':category,'new_expert_count':new_expert_count,'rebooking_count':rebooking_count,'customer_count':customer_count})

def add_category(request):
    if request.method == "POST":
        
        category_name = request.POST.get('category_name')
        
        
        
        if Category.objects.filter(category_name = category_name).exists():
            # return JsonResponse({'status': 'error', 'message': 'Category is already Taken'})
            messages.warning(request,f'{category_name} already Exists')
            return redirect('category')
            
        category = Category.objects.create(category_name=category_name)
        category.save()
        messages.success(request,f'{category_name} Add Successfully')
        return redirect('category')
       
        
        # return JsonResponse({'status':'Save','cat_Data':cat_Data})


def delete_Category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request,"Records are Successfully Deleted")
    return redirect('category')

def edit_Category(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')
        category = Category.objects.get(id=category_id) 
        category.category_name = category_name
        category.save()
        messages.success(request,"Records are Updated Successfully")
        return redirect('category')

def subcategory(request):
    category = Category.objects.all()
    sub_category = SubCategory.objects.all()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == 'POST':
        category_id = request.POST.get('category_id')

        
        subcategory_names = request.POST.getlist('subcategory_name[]')
        ctg_id = Category.objects.get(id=category_id)
        
        for name in subcategory_names:
            subcategory = SubCategory.objects.create(Category_id=ctg_id, name=name)
            subcategory.save()
            

    context = {
        'category':category,
        'sub_category':sub_category,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }
    
    return render(request,'homofix_app/AdminDashboard/Subcategory/sub_category.html',context)

def edit_subcategory(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id')
        sub_category_id = request.POST.get('sub_category_id')
        sub_category_name = request.POST.get('sub_category_name')

        category = Category.objects.get(id=category_id)
        
        subcategory = SubCategory.objects.get(id=sub_category_id) 
        subcategory.Category_id= category
        subcategory.name= sub_category_name
        subcategory.save()
        messages.success(request,"Records are Updated Successfully")
        return redirect('subcategory')
def delete_subcategory(request,id):
    subcategory = SubCategory.objects.get(id=id)
    subcategory.delete()
    messages.success(request,"Deleted")
    return redirect('subcategory')

def technician(request):
    category = Category.objects.all()
    technician = Technician.objects.filter(status="Active")
    # user_status = {}
    # for user in technician:
    #     # check if user is logged in by looking at their last login time
    #     if user.admin.last_login is not None and timezone.now() - user.admin.last_login < timezone.timedelta(seconds=1):
    #         # user is online
    #         user_status[user.id] = 'online'
    #     else:
    #         # user is offline
    #         user_status[user.id] = 'offline'
    # print("user status",user_status)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        
        category_id = request.POST.get('category_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       

        ctg = Category.objects.get(id=category_id)
        
      
        if CustomUser.objects.filter(username = username).exists():
            # return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
            messages.error(request,'Username is already Taken')
            return redirect('technician')
            
        user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type='2')
        user.technician.category = ctg
        user.save()
        messages.success(request,'Technician Register Successfully')
        # if(user.is_active):
        #     return JsonResponse({'status':'Save'})
            
        # else:
        #     return JsonResponse({'status':0})

    return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count})




def add_technician(request):
    
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    if request.method == "POST":
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        
        sub_category_id = request.POST.getlist('sub_category_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        subcat = SubCategory.objects.filter(id__in=sub_category_id)
        user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=first_name+unique_number,password=password,email=email,user_type='2')
        user.technician.subcategories.set(subcat)
        user.save()
        messages.success(request,'Technician Register Successfully')
        return redirect('technician')
       

    context = {
        'category':category,
        'subcategory':subcategory,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
    }
    return render(request,'homofix_app/AdminDashboard/Technician/add_technician.html',context)

def technician_add_category(request):
    if request.method == "POST":
        
        category_name = request.POST.get('category_name')
        
        
        
        if Category.objects.filter(category_name = category_name).exists():
            # return JsonResponse({'status': 'error', 'message': 'Category is already Taken'})
            messages.warning(request,f'{category_name} already Exists')
            return redirect('technician')
            
        category = Category.objects.create(category_name=category_name)
        category.save()
        messages.success(request,f'{category_name} Add Successfully')
        return redirect('technician')



def technician_edit_profile(request,id):
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    technician = Technician.objects.get(id=id)
    state_choices = STATE_CHOICES
    sub_cat = SubCategory.objects.all()

   
    category = Category.objects.all()
    # subcategories = SubCategory.objects.all()
    subcategories = SubCategory.objects.filter(Category_id__id__in=technician.subcategories.values_list('Category_id__id', flat=True))
    # print("subcategory",subcategories)
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
   
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
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
        technician.admin.first_name = first_name
        technician.admin.last_name = last_name
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
        
        elif status == 'New':
            technician.status = 'New'

        else:
            technician.status = 'Active'

        technician.rating=rating
        technician.serving_area=serving_area
        technician.highest_qualification=highest_qualification
        technician.state=state
        technician.subcategories.set(subcategory_id)
       
        if city:
            city = city.lower()
        technician.city=city
        # technician.joining_date=date_of_joining
        if date_of_joining:
            technician.joining_date =date_of_joining
        if application_form != None:
            technician.application_form=application_form
        

        # cat = Category.objects.get(id=category_id)
        # if subcategory_id:
        #     subcategories = SubCategory.objects.filter(id__in=subcategory_id)
        #     technician.subcategories.set(subcategories)
           

        technician.admin.save()
        technician.save()
        messages.success(request,'updated sucessfully')
        return redirect('technician_edit_profile',id=technician.id)
        # return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})
        # return redirect('technician_edit_profile',{'technician_id': technician_id})
    return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category,'subcategories': subcategories,'state_choices':state_choices,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count })


def edit_technician(request):
    if request.method == "POST":
        
        technician_id = request.POST.get('technician_id')
        category_id = request.POST.get('category_id')
        username = request.POST.get('username')
        email = request.POST.get('email')


        technician = Technician.objects.get(id=technician_id)
        technician.admin.username = username
        technician.admin.email = email

        
        technician.category = Category.objects.get(id=category_id)
        technician.admin.save()
        technician.save()
        
        
        messages.success(request,"Records are Updated Successfully")
        return redirect('technician')

def delete_technician(request,id):
    technician = Technician.objects.get(id=id)
    user = technician.admin
    technician.delete()
    user.delete()
    messages.success(request, "Technician deleted successfully.")
    return redirect('technician')


def technician_history(request,id):
    task = Task.objects.filter(technician=id)
    rebooking = Rebooking.objects.filter(technician=id)
    technician = Technician.objects.get(id=id)
    tecnician_location = TechnicianLocation.objects.filter(technician_id=technician)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'task':task,
        'rebooking':rebooking,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'tecnician_location':tecnician_location
    }
   
    return render(request,'homofix_app/AdminDashboard/History/task_history.html',context)
   

# def technician_payment_history(request,id):

#     technician = Technician.objects.get(id=id)
#     wallet_history = WalletHistory.objects.filter(wallet__technician=technician)
    
    
#     share = Share.objects.filter(task__technician=technician)
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     rebooking_count = Rebooking.objects.all().count()
#     customer_count = Customer.objects.all().count() 
    
#     wallet = Wallet.objects.get(technician=technician) 
    

#     if request.method == "POST":
        
#         type = request.POST.get('type')
#         amount = int(request.POST.get('amount'))
#         description = request.POST.get('description')

#         history = WalletHistory(wallet=wallet,type=type,amount=amount,description=description)
#         if history.type == 'bonus':
#             wallet.total_share += history.amount
#         else:
#             wallet.total_share -= history.amount
#         wallet.save()
#         history.save()
#         messages.success(request, f"{'Wallet Add  Successfully'}")
#         return redirect('technician_payment_history',technician.id)
        
        
    


#     context = {
        
#         'new_expert_count':new_expert_count,
#         'booking_count':booking_count,
#         'rebooking_count':rebooking_count,
#         'customer_count':customer_count,
#         'share':share,
#         'wallet_history':wallet_history,
#         'wallet':wallet
#     }
   
#     return render(request,'homofix_app/AdminDashboard/History/ExpertPaymentHistory/expert_payment_history.html',context)


def technician_payment_history(request,id):

    technician = Technician.objects.get(id=id)
    
    
    wallet_history = WalletHistory.objects.filter(wallet__technician_id=technician)
   
    share = Share.objects.filter(task__technician=technician)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count() 
    
    try:
       
        wallet = Wallet.objects.get(technician_id=technician)
        
    except Wallet.DoesNotExist:
        wallet = None
        messages.warning(request, 'No wallet found for this technician.')
    try:
        kyc = Kyc.objects.filter(technician_id=technician)
    except Kyc.DoesNotExist:
        kyc = None
        messages.warning(request, 'No KYC found for this technician.')

    if request.method == "POST":
        
        type = request.POST.get('type')
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description')

        if wallet:
            history = WalletHistory(wallet=wallet,type=type,amount=amount,description=description)
            if history.type == 'bonus':
                wallet.total_share += Decimal(str(history.amount))
            else:
                wallet.total_share -= Decimal(str(history.amount))
            wallet.save()
            history.save()
            messages.success(request, 'Wallet transaction successfully added.')
        else:
            messages.warning(request, 'No wallet found for this technician.')
        
        return redirect('technician_payment_history',technician.id)
        
        
    


    context = {
        
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'share':share,
        'wallet_history':wallet_history,
        'wallet':wallet,
        'kyc':kyc
    }
   
    return render(request,'homofix_app/AdminDashboard/History/ExpertPaymentHistory/expert_payment_history.html',context)



    # return render(request,'homofix_app/AdminDashboard/History/ExpertPaymentHistory/expert_payment_history.html',context)
    
    # wallet = Wallet.object.get(technician=id)
    # technician = Technician.objects.get(id=wallet)
    # print("technician id",technician)
    # return redirect('technician_payment_history',technician.id)  

def product(request):
    product = Product.objects.all()
    category = Category.objects.all()
    categories = Category.objects.all()
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_pic = request.FILES.get("product_pic")
        product_name = request.POST.get("product_name")
        product_title = request.POST.get("product_title")
        price = int(request.POST.get("price"))
        discount_amt = int(request.POST.get("discount_amt"))
        warranty = request.POST.get("warranty")
        description = request.POST.get("desc")
        warranty_desc = request.POST.get("warranty_desc")
        # category_id = request.POST.get("category_id")
        sub_category_id = request.POST.get("sub_category_id")

        

        if Product.objects.filter(name=product_name).exists():
            messages.warning(request, "Product is already taken")
            return redirect("product")

        # cat = Category.objects.get(id=category_id)
        subcategry = SubCategory.objects.get(id=sub_category_id)
        product = Product.objects.create(
            product_pic=product_pic,
            name=product_name,
            product_title=product_title,
            # category=cat,
            price=price,
            warranty=warranty,
            warranty_desc=warranty_desc,
            description=description,
            subcategory=subcategry,
            dis_amt=discount_amt

            
        )
        messages.success(request, "Product added successfully")
        product.save()
        return redirect("product")

    context = {
        "product": product,
        "category": category,
        "new_expert_count": new_expert_count,
        "booking_count": booking_count,
        "subcategory": subcategory,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'categories':categories
    }
    return render(request, "homofix_app/AdminDashboard/Product/product.html", context)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    print("category_id",category_id)
    subcategories = SubCategory.objects.filter(Category_id=category_id)
   
    data = list(subcategories.values('id', 'name'))
    return JsonResponse(data, safe=False)




def get_products(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        subcategory_id = int(subcategory_id)
        products = Product.objects.filter(subcategory_id=subcategory_id)
        data = [{'id': product.id, 'name': product.name} for product in products]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)



def get_products_price(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        subcategory_id = int(subcategory_id)
        products = Product.objects.filter(subcategory_id=subcategory_id)
        data = []
        for product in products:
            if product.selling_price is not None:
                price = product.selling_price
            else:
                price = product.price
            data.append({'id': product.id, 'price': price, 'name': product.name})
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)
# def product(request):
    

#     product = Product.objects.all()
#     category = Category.objects.all()
#     subcategory = SubCategory.objects.all()
#     new_expert_count = Technician.objects.filter(status="New").count()
#     booking_count = Booking.objects.filter(status = "New").count()
#     if request.method == "POST":       
        
#         product_pic = request.FILES.get('product_pic')
#         product_name = request.POST.get('product_name')
#         product_title = request.POST.get('product_title')
#         price = request.POST.get('price')
#         warranty = request.POST.get('warranty')
#         description = request.POST.get('desc')
#         warranty_desc = request.POST.get('warranty_desc')
#         category_id = request.POST.get('category_id')
       
        
        
#         if Product.objects.filter(name = product_name).exists():
#             # return JsonResponse({'status': 'error', 'message': 'Product is already Taken'})
#             messages.warning(request,'Product is already Taken')
#             return redirect('product')
            
#         cat = Category.objects.get(id=category_id)
#         product = Product.objects.create(product_pic=product_pic,name=product_name,product_title=product_title,category=cat,price=price,warranty=warranty,warranty_desc=warranty_desc,description=description)
#         messages.success(request,'Product Add Successfully')
#         product.save()
#         return redirect('product')
        
#         # return JsonResponse({'status':'Save'})
#     return render(request,'homofix_app/AdminDashboard/Product/product.html',{'product':product,'category':category,'new_expert_count':new_expert_count,'booking_count':booking_count,'subcategory':subcategory})


def update_product(request):
    if request.method == "POST":
        
        product_id = request.POST.get('product_id')
        # category_id = request.POST.get('category_id')
        subcategory_id = request.POST.get('subcategory_id')
        product_pic = request.FILES.get('product_pic')

        product_title = request.POST.get('product_title')
        product_name = request.POST.get('product_name')
        price = int(request.POST.get('price'))
        discount_price = int(request.POST.get('discount_price'))
        warranty = request.POST.get('warranty')
        warranty_description = request.POST.get('warranty_description')
        description = request.POST.get('description')

        # print("description",description)

        print("disocunt price",discount_price)
        # cat = Category.objects.get(id=category_id)
        subcat = SubCategory.objects.get(id=subcategory_id)
        product = Product.objects.get(id=product_id)
        
        discountd_price = price - discount_price

        # print("sellling price",discountd_price)
        if product_pic != None:
            product.product_pic = product_pic
        product.subcategory = subcat
        product.product_title = product_title
        product.name = product_name
        product.price = price
        product.dis_amt = discount_price
        product.selling_price = price - discount_price
        product.warranty = warranty
        product.warranty_desc = warranty_description
        product.description = description

        product.save()
        
        
        messages.success(request,"Records are Updated Successfully")
        return redirect('product')



def delete_product(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect('product')





######################## Addons #####################


def addons(request):
    category = Category.objects.all()
    addons = SpareParts.objects.all()
    product = Product.objects.all()
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        spare_part = request.POST.get('spare_part')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        prod = Product.objects.get(id=product_id)
        addon = SpareParts.objects.create(product=prod,spare_part=spare_part,price=price,description=desc)
        
        messages.success(request,'Addons Product Add Successfully')
        return redirect('addons')
        

    return render(request,'homofix_app/AdminDashboard/Addons/addon.html',{'addons':addons,'product':product,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count,'category':category,'subcategory':subcategory})


def edit_addons(request,id):
    
    spare_parts = SpareParts.objects.get(id=id)
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    product = Product.objects.all()
    context = {
        'spare_parts':spare_parts,
        'category':category,
        'subcategory':subcategory,
        'product':product
    }
    return render(request,'homofix_app/AdminDashboard/Addons/edit_addons.html',context)

def update_addons(request):

    if request.method == "POST":
        addon_id  = request.POST.get('spare_parts_id')
        print("addon id",addon_id)
        product_id  = request.POST.get('product_id')
        spare_part  = request.POST.get('spare_part')
        price  = request.POST.get('price')
        description  = request.POST.get('desc')
  
        product = Product.objects.get(id=product_id)
        addons_prod = SpareParts.objects.get(id=addon_id)
        
        addons_prod.product = product
        addons_prod.spare_part = spare_part
        addons_prod.price = price
        addons_prod.description =description
        
        addons_prod.save()
        messages.success(request,'SpareParts Updated Successfully')
        return redirect('addons')

    

def delete_addons(request,id):

    addon = SpareParts.objects.get(id=id)
    addon.delete()
    messages.success(request, "Addon deleted successfully.")
    return redirect('addons')

def addons_details(request):
    addon = Addon.objects.all()
    context = {
        'addon':addon
    }
    return render(request,'homofix_app/AdminDashboard/Addons/addons_detail.html',context)


# --------------------- SUPPORT CREATION --------------------- 

def support(request):
    suppt = Support.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    return render(request,'homofix_app/AdminDashboard/Support/support.html',{'suppt':suppt,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count})

def add_support(request):
    
    if request.method == "POST":
        random_number = random.randint(0, 999)
        unique_number = str(random_number).zfill(3)
        # username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        can_new_booking = request.POST.get('new_booking')
        can_cancel_booking = request.POST.get('can_cancel_booking')
        can_rebooking = request.POST.get('can_rebooking')
        can_assign_task = request.POST.get('can_assign_task')
        can_new_expert = request.POST.get('can_new_expert')
        print("new expert",can_new_expert)
        can_customer_enquiry = request.POST.get('can_customer_enquiry')
        
        # if CustomUser.objects.filter(username=username).exists():
        #     messages.error(request, 'Username is already taken')
        #     return redirect('admin_support')
            
        user = CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=first_name+unique_number, password=password, email=email, user_type='3')
        user.support.can_new_booking = True if can_new_booking == 'on' else False
        user.support.can_cancel_booking = True if can_cancel_booking == 'on' else False
        user.support.can_rebooking = True if can_rebooking == 'on' else False
        user.support.can_assign_task = True if can_assign_task == 'on' else False
        user.support.can_expert_create = True if can_new_expert == 'on' else False
        user.support.can_contact_us_enquiry = True if can_customer_enquiry == 'on' else False
        
        user.save()
        messages.success(request, 'Support registered successfully')
        return redirect('admin_support')
        
    return redirect('admin_support')


def support_profile(request,id):
    
    support = Support.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    return render(request,'homofix_app/AdminDashboard/Support/edit_profile.html',{'support':support,'new_expert_count':new_expert_count,'rebooking_count':rebooking_count,'customer_count':customer_count})


# def support_update_profile(request):
    
#     if request.method == "POST":
#         support_id = request.POST.get('support_id')
       
#         profile_pic = request.FILES.get('profile_pic') 
#         username = request.POST.get('username')
#         father_name = request.POST.get('father_name')
#         marital_status = request.POST.get('marital_status')
#         dob = request.POST.get('dob')
#         email = request.POST.get('email')
#         mob_no = request.POST.get('mob_no')
#         address = request.POST.get('address')
#         permanent_address = request.POST.get('permanent_address')
#         date_of_joining = request.POST.get('date_of_joining')
#         status = request.POST.get('status')
#         xyzzz = request.POST.get('xyzzz')
#         firstname = request.POST.get('firstname')
#         print("last name",xyzzz)
        
#         application_form = request.FILES.get('application_form')
#         document_form = request.FILES.get('document_form')
#         # print("application form", application_form)


#         # Permission 
#         can_new_booking = request.POST.get('new_booking')
#         can_cancel_booking = request.POST.get('can_cancel_booking')
#         can_rebooking = request.POST.get('can_rebooking')
#         can_assign_task = request.POST.get('can_assign_task')
#         can_new_expert = request.POST.get('can_new_expert')
#         can_customer_enquiry = request.POST.get('can_customer_enquiry')
#         can_job_enquiry = request.POST.get('can_job_enquiry')

#         support = Support.objects.get(id=support_id)
#         print("suppor id ",support)
#         support.admin.last_name = xyzzz
#         support.admin.last_name="dd"
#         support.save()
        
        
#         if profile_pic:
#             support.profile_pic = profile_pic
        
#         if application_form:
#             support.application_form=application_form

#         if document_form:
#             support.document_form=document_form

        
#         # if application_form:
#         #     application_form_str = ','.join(str(file) for file in application_form)
#         #     support.application_form = application_form_str
#         print("helooooo first",support.admin.first_name) 
#         print("helooooo last",support.admin.last_name) 
#         # support.admin.last_name = lastname 
#         # support.admin.username = username 
#         # support.admin.email = email
#         # support.admin.last_name = last_name 
#         support.admin.first_name = firstname 
#         support.address = address 
#         support.permanent_address = permanent_address 
#         support.father_name = father_name 
#         support.marital_status = marital_status 
#         support.d_o_b = dob 
#         support.mobile = mob_no 


#         support.can_new_booking = True if can_new_booking == 'on' else False
#         support.can_cancel_booking = True if can_cancel_booking == 'on' else False
#         support.can_rebooking = True if can_rebooking == 'on' else False
#         support.can_assign_task = True if can_assign_task == 'on' else False
#         support.can_expert_create = True if can_new_expert == 'on' else False
#         support.can_contact_us_enquiry = True if can_customer_enquiry == 'on' else False
#         support.can_job_enquiry = True if can_job_enquiry == 'on' else False


#         if date_of_joining:
#             support.joining_date = date_of_joining 

#         if status == 'Deactivate':
#             support.status = "Deactivate"
#         elif status == 'Hold':
#             support.status = 'Hold'
#         else:
#             support.status = 'Active'

        
#         support.save()
#         messages.success(request, 'Support Updated Succesffully')
#         return HttpResponseRedirect(reverse("support_profile",args=[support_id]))



def support_update_profile(request):
    if request.method == "POST":
        support_id = request.POST.get('support_id')
        support_nw_id = request.POST.get('support_nw_id')
        print("fadsfadsfadsfads",support_nw_id)
       
        profile_pic = request.FILES.get('profile_pic') 
        username = request.POST.get('username')
        father_name = request.POST.get('father_name')
        marital_status = request.POST.get('marital_status')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        address = request.POST.get('address')
        permanent_address = request.POST.get('permanent_address')
        date_of_joining = request.POST.get('date_of_joining')
        status = request.POST.get('status')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        
        application_form = request.FILES.get('application_form')
        document_form = request.FILES.get('document_form')
        # print("application form", application_form)


        # Permission 
        can_new_booking = request.POST.get('new_booking')
        can_cancel_booking = request.POST.get('can_cancel_booking')
        can_rebooking = request.POST.get('can_rebooking')
        can_assign_task = request.POST.get('can_assign_task')
        can_new_expert = request.POST.get('can_new_expert')
        can_customer_enquiry = request.POST.get('can_customer_enquiry')
        can_job_enquiry = request.POST.get('can_job_enquiry')

        # support = Support.objects.get(id=support_id)
        hod = CustomUser.objects.get(id=support_id)
        
        
        if profile_pic:
            hod.profile_pic = profile_pic
        
        if application_form:
            hod.support.application_form=application_form

        if document_form:
            hod.support.document_form=document_form

        
        # if application_form:
        #     application_form_str = ','.join(str(file) for file in application_form)
        #     support.application_form = application_form_str
        # print("helooooo",support.admin.first_name) 
        # support.admin.last_name = lastname 
        # support.admin.username = username 
        # support.admin.email = email
        hod.first_name = firstname 
        hod.last_name = lastname 
        hod.support.address = address 
        hod.support.permanent_address = permanent_address 
        hod.support.father_name = father_name 
        hod.support.marital_status = marital_status 
        hod.support.d_o_b = dob 
        hod.support.mobile = mob_no 


        hod.support.can_new_booking = True if can_new_booking == 'on' else False
        hod.support.can_cancel_booking = True if can_cancel_booking == 'on' else False
        hod.support.can_rebooking = True if can_rebooking == 'on' else False
        hod.support.can_assign_task = True if can_assign_task == 'on' else False
        hod.support.can_expert_create = True if can_new_expert == 'on' else False
        hod.support.can_contact_us_enquiry = True if can_customer_enquiry == 'on' else False
        hod.support.can_job_enquiry = True if can_job_enquiry == 'on' else False


        if date_of_joining:
            hod.support.joining_date = date_of_joining 

        if status == 'Deactivate':
            hod.support.status = "Deactivate"
        elif status == 'Hold':
            hod.support.status = 'Hold'
        else:
            hod.support.status = 'Active'

        
        hod.save()
        messages.success(request, 'Support Updated Succesffully')
        return HttpResponseRedirect(reverse("admin_support_profile",args=[support_nw_id]))


def delete_support(request,id):
    support = Support.objects.get(id=id)
    user = support.admin
    support.delete()
    user.delete()
    messages.success(request, "Support deleted successfully.")
    return redirect('admin_support')
    
def support_history(request,id):
    support = Support.objects.get(id=id)
    task = Task.objects.filter(supported_by=support,booking__status='Assign')
    technician = Technician.objects.filter(supported_by=support)
    print("ddddd",technician)

    booking = Booking.objects.filter(supported_by=id)    
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'booking':booking,
        'task':task,
        'technician':technician
        
    }
    return render(request,'homofix_app/AdminDashboard/History/SupportHistory/support_history.html',context)


# ------------------------------- FAQS ------------------------------        



def add_faq(request):
    product = Product.objects.all()
    category = Category.objects.all()
    subcategory =SubCategory.objects.all()
    faqs = FAQ.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        prod_id = Product.objects.get(id=product_id)
        faq = FAQ.objects.create(product=prod_id,question=question,answer=answer)
        faq.save()
        
    context = {
        'product':product,
        'faqs':faqs,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'category':category,
        'customer_count':customer_count,
        'subcategory':subcategory
    }

    return render(request,'homofix_app/AdminDashboard/Faqs/faqs.html',context)

def update_add_faq(request):
    if request.method == "POST":
        faq_id = request.POST.get('faq_id')
        product_id = request.POST.get('product_id')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        prod_id = Product.objects.get(id=product_id)
        faq = FAQ.objects.get(id=faq_id)
        faq.product = prod_id
        faq.question = question
        faq.answer = answer
        faq.save()
        messages.success(request,'FAQ Updated Successfully')
        return redirect('add_faq')



def delete_faq(request,id):
    faq = FAQ.objects.get(id=id)
    faq.delete()
    messages.success(request, " FAQ deleted successfully.")
    return redirect('add_faq')



def booking_list(request):
    booking_count = Booking.objects.filter(status = "New").count()
    booking = Booking.objects.all()
    bookings = Booking.objects.filter(status="New")
    
    technicians = Technician.objects.all()
    tasks = Task.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        
        otp_number = random.randint(0,9999)
        otp_unique = str(otp_number).zfill(3)
       
        first_name = request.POST.get('full_name')      
        mob = request.POST.get('mob')
        request.session['full_name'] = first_name
        request.session['mob'] = mob
        request.session['otp'] = otp_unique

        if Customer.objects.filter(mobile=mob).exists():
            print("helloooo suceess")
            # print("heloooooooo")
            


            # auth_key = "IQkJfqxEfD5l3qCu"
            # sender_id = "TRYGON"
            # route = 2
            # number = mob
       
            # message = f"Dear {first_name} {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
            
            
            # template_id = "1707162192151162124"
            # url = f"http://weberleads.in/http-tokenkeyapi.php?authentic-key={auth_key}&senderid={sender_id}&route={route}&number={number}&message={urllib.parse.quote(message)}&templateid={template_id}"
            # response = requests.get(url) 
                

            return JsonResponse({'status':'Save'})

        # elif Customer.objects.filter(mobile=mob).exists():
        #     print("hellooooo")
        #     return JsonResponse({'status':'Error'})

            
        else:
            
        

            # request.session['full_name'] = first_name
            # request.session['mob'] = mob
            # request.session['otp'] = otp_unique


            # auth_key = "IQkJfqxEfD5l3qCu"
            # sender_id = "TRYGON"
            # route = 2
            # number = mob
        
            # message = f"Dear {first_name} {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
        
        
            # template_id = "1707162192151162124"
            # url = f"http://weberleads.in/http-tokenkeyapi.php?authentic-key={auth_key}&senderid={sender_id}&route={route}&number={number}&message={urllib.parse.quote(message)}&templateid={template_id}"
            # response = requests.get(url) 
                    

            return JsonResponse({'status':'Save'})
        
        
        
  
    # return render(request, 'Support_templates/Orders/order.html',context)

    context = {
    'booking':booking,
    'technicians':technicians,
    'tasks':tasks,
    'new_expert_count':new_expert_count,
    'booking_count':booking_count,
    'rebooking_count':rebooking_count,
    'customer_count':customer_count,
    'bookings':bookings,
    
    
    
    
   }
    
    
    
    return render(request,'homofix_app/AdminDashboard/Booking_list/booking.html',context)    



def admin_verify_otp(request):
    if request.method == "POST":
        
        otp_num = request.session.get('otp', 'Default value if key does not exist')
        
        

        otp = request.POST.get('otp')
        # if otp == otp_num:  
        if otp == "1234":  
            # OTP is correct, redirect to success page
            # return HttpResponse('otp sucess')
            
            random_number = random.randint(0, 999)
            unique_number = str(random_number).zfill(3)
       
            first_name = request.session.get('full_name', 'Default value if key does not exist')
            mob = request.session.get('mob', 'Default value if key does not exist')
            
            
            if Customer.objects.filter(mobile=mob).exists():
                customer = Customer.objects.get(mobile=mob)
                request.session['customer_id'] = customer.id
                # request.session['customer_id'] = Customer.id
                return JsonResponse({'status': 'Save', 'message': 'otp is match'})
                
            else:

                # user = CustomUser.objects.create(username=user.id,first_name=first_name, user_type='4')    
                user = CustomUser.objects.create(first_name=first_name,username=first_name+unique_number, user_type='4')    
                user.set_password(mob)
                user.customer.mobile = mob
                user.save()
                request.session['customer_id'] = user.customer.id

            return JsonResponse({'status': 'Save', 'message': 'otp is match'})
            # return redirect('support_orders')
        else:
            print("show error msg here")
            return JsonResponse({'status': 'Error', 'message': 'otp is match'})
            # OTP is incorrect, show error message and reload the page
            # messages.error(request, 'Invalid OTP. Please try again.')
            
            # return JsonResponse({'status': 'Error', 'message': 'otp is not  valid'})
    


# def admin_booking(request):
   
    
#     user = request.user
#     adminhod = AdminHOD.objects.get(admin=user)
#     admin_by = request.user.adminhod
    
#     prod = Product.objects.all()
#     category = Category.objects.all()
#     state_choices = STATE_CHOICES
    
    

#     if request.method == 'POST':
       
#         customer_id = request.session.get('customer_id','Default value if key does not exist')
#         print("customer id ",customer_id)
        
#         product_ids = request.POST.getlist('product_id')
#         quantities = request.POST.getlist('quantity')

#         print("qunattttiyttt",quantities)
        
#         booking_date_str = request.POST.get('booking_date')
#         state = request.POST.get('state')
#         zip_code = request.POST.get('zip_code')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         area = request.POST.get('area')
#         description = request.POST.get('description')
#         total_amount = int(request.POST.get('total_amount'))
#         print("sss",total_amount)
        
#         customer = Customer.objects.get(id=customer_id)
#         if city:
#             city = city.lower()
#         customer.city = city
#         customer.state = state
#         customer.area = area
#         customer.zipcode = zip_code
#         customer.address=address,
#         customer.save()
#         booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        
        
#         booking = Booking.objects.create(
#             customer=customer,
#             booking_date=booking_date,   
#             description=description,          
#             admin_by=admin_by
           
#         )



#         for i, product_id in enumerate(product_ids):
#             product = Product.objects.get(id=product_id)
#             print("producttttt",product)
#             # print("producttttt",product)
            
#             quantity = int(quantities[i])
#             print("quaaaaaa",quantity)
#             price = int(request.POST.getlist('price')[i])
            
#             BookingProduct.objects.create(
#                 booking=booking,
#                 product=product,
#                 quantity=quantity,
#                 total_price=total_amount
#                 # price=price
#             )
#             # total_price = sum(price_list)
#             # booking.total_price = total_price
#             booking.save()

#         messages.success(request, 'Booking created successfully.')
#         return redirect('booking_list')

#     context = {
#         'prod': prod,
#         'state_choices':state_choices,
#         'category':category,
#         'support':support
#     }
#     return render(request, 'homofix_app/AdminDashboard/Booking_list/create_booking.html', context)


# def admin_booking(request):
#     user = request.user
#     adminhod = AdminHOD.objects.get(admin=user)
#     admin_by = request.user.adminhod
    
#     prod = Product.objects.all()
#     category = Category.objects.all()
#     state_choices = STATE_CHOICES
    
#     if request.method == 'POST':
#         customer_id = request.session.get('customer_id','Default value if key does not exist')
#         product_ids = request.POST.getlist('product_id')
        
        
#         quantities = request.POST.getlist('quantity')
        
#         # for i in range(len(product_ids)):
#         #     print("Product ID:", product_ids[i])
#         #     print("Quantity:", quantities[i])
#         print("qantityyyyy",quantities)
#         booking_date_str = request.POST.get('booking_date')
#         state = request.POST.get('state')
#         zip_code = request.POST.get('zip_code')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         area = request.POST.get('area')
#         description = request.POST.get('description')
#         total_amount = int(request.POST.get('total_amount'))
        
#         customer = Customer.objects.get(id=customer_id)
#         if city:
#             city = city.lower()
#         customer.city = city
#         customer.state = state
#         customer.area = area
#         customer.zipcode = zip_code
#         customer.address=address,
#         customer.save()
#         booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        
#         booking = Booking.objects.create(
#             customer=customer,
#             booking_date=booking_date,   
#             description=description,          
#             admin_by=admin_by
#         )

#         for i, product_id in enumerate(product_ids):
#             product = Product.objects.get(id=product_id)
#             quantity = int(quantities[i])
#             print("qunatittt",quantity)
#             price = int(request.POST.getlist('price')[i])
            
#             BookingProduct.objects.create(
#                 booking=booking,
#                 product=product,
#                 quantity=quantity,
#                 total_price=price * quantity
#             )

#         messages.success(request, 'Booking created successfully.')
#         return redirect('booking_list')

#     context = {
#         'prod': prod,
#         'state_choices':state_choices,
#         'category':category,
#         'support':support
#     }
#     return render(request, 'homofix_app/AdminDashboard/Booking_list/create_booking.html', context)


def admin_booking(request):
   
    
    user = request.user
    adminhod = AdminHOD.objects.get(admin=user)
    admin_by = request.user.adminhod
    
    prod = Product.objects.all()
    category = Category.objects.all()
    state_choices = STATE_CHOICES
    
    

    if request.method == 'POST':
       
        customer_id = request.session.get('customer_id','Default value if key does not exist')
        print("customer id ",customer_id)
        
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
        print("sss",total_amount)
        
        customer = Customer.objects.get(id=customer_id)
        if city:
            city = city.lower()
        customer.city = city
        customer.state = state
        customer.area = area
        customer.zipcode = zip_code
        customer.address=address,
        customer.save()
        booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        
        
        booking = Booking.objects.create(
            customer=customer,
            booking_date=booking_date,   
            description=description,          
            admin_by=admin_by
           
        )



        for i, product_id in enumerate(product_ids):
            product = Product.objects.get(id=product_id)
            print("producttttt",product)
            # print("producttttt",product)
            
            quantity = int(quantities[i])
            print("quaaaaaa",quantity)
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
        return redirect('booking_list')

    context = {
        'prod': prod,
        'state_choices':state_choices,
        'category':category,
        'support':support
    }
    return render(request, 'homofix_app/AdminDashboard/Booking_list/create_booking.html', context)



def admin_List_of_expert(request,id):
    # user = request.user
    # support = Support.objects.get(admin=user)  
    
    booking = Booking.objects.get(id=id)
    
   
    expert = Technician.objects.filter(city=booking.customer.city)
    tasks = Task.objects.filter(booking=booking)
    
   
    
    # expert = Technician.objects.filter(city=booking.city, serving_area__icontains=booking.area)
    context = {
        'expert':expert,
        'booking':booking,
        'tasks': tasks,
        'support':support
        
        
        
    }
    
    return render(request,'homofix_app/AdminDashboard/Booking_list/list_of_expert.html',context)    

def admin_reschedule(request):
    if request.method == "POST":

        booking_id=request.POST.get('booking_id')
        booking_date_str = request.POST.get('booking_date')
        booking_date = timezone.make_aware(datetime.datetime.fromisoformat(booking_date_str))
        print("booking date",booking_date)
        booking = Booking.objects.get(id=booking_id)
        booking.booking_date = booking_date
        booking.save()
        messages.success(request,"Your order reschedule success")

       

        return redirect('booking_list')




def cancel_booking_byadmin(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking has been cancelled.')
    return redirect('booking_list')    


def task_assign(request):
    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        technician_id = request.POST.get('technician_id')

        booking = Booking.objects.get(id=booking_id)
        technician = Technician.objects.get(id=technician_id)
        
        print("BOOKING ID",booking_id)
        print("technician_id",technician_id)
        task = Task.objects.create(booking=booking,technician=technician)
        task.save()
        booking.status = "Assign"
        booking.save()

        messages.success(request,'Assign Task Successfully')
        return redirect('booking_list')
    # 
    # print("technician id",tect_id)
    return redirect('booking_list')


def list_of_task(request):
    task = Task.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'task':task,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
        
    }
    return render(request,'homofix_app/AdminDashboard/Booking_list/task.html',context)    


def Listofcancel(request):
    booking = Booking.objects.filter(status="cancelled")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    context = {
        'booking':booking,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }
    return render(request,'homofix_app/AdminDashboard/Booking_list/cancel_booking.html',context)    


def ListofNewExpert(request):
    category = Category.objects.all()
    technician = Technician.objects.filter(status="New")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    context = {
        'category' :category,
        'technician':technician,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }
    return render(request,'homofix_app/AdminDashboard/Notification/New_expert.html',context)



def Listofrebooking(request):
    rebooking = Rebooking.objects.all()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    
    
    context = {
        'rebooking':rebooking,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count
        
    }

    return render(request,'homofix_app/AdminDashboard/Rebooking/list_of_rebooking.html',context)



def admin_booking_complete(request):
    
   
    task = Task.objects.filter(booking__status = "Completed")
    context = {
        'task':task,
        
        
    }
    return render(request,'homofix_app/AdminDashboard/Rebooking/booking_complete.html',context)    


def admin_rebooking(request, task_id):
    
    task = get_object_or_404(Task, id=task_id)
    booking_id = task.booking.id
    
    
    
    # user = request.user
    # support = Support.objects.get(admin=user)
    
    booking_products = BookingProduct.objects.filter(booking_id=booking_id).select_related('booking', 'product')
    
    for booking_product in booking_products:
        rebookings = Rebooking.objects.filter(booking_product_id=booking_product.id).order_by('-id')
        booking_product.rebookings.set(rebookings)

    context = {
        'booking_prod': booking_products,
        'support':support,
        'task':task
        
    }
    return render(request, 'homofix_app/AdminDashboard/Rebooking/rebooking.html', context)


def admin_rebooking_update(request):
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
        # task.booking.status = "completed"
        # task.booking.save()
        
        rebooking.save()
        print("successsss",rebooking)
        messages.success(request, 'Rebooking successfully created.')
        return redirect('admin_booking_complete')

    context = {}
    return render(request, 'homofix_app/AdminDashboard/Rebooking/booking_complete.html', context)


def contactus(request):
    contact_us = ContactUs.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'contact_us':contact_us,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        
    }

    return render(request,'homofix_app/AdminDashboard/Contactus/contact_us.html',context)

def admin_job_enquiry(request):
    job_enquiry = JobEnquiry.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'job_enquiry':job_enquiry,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        
    }

    return render(request,'homofix_app/AdminDashboard/JobEnquiry/job_enquiry.html',context)



def admin_share_percentage(request):
    share_percentage = HodSharePercentage.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        share_amt = request.POST.get('share_amt')
        share = HodSharePercentage.objects.create(percentage=share_amt)
        share.save()
        messages.success(request,'Share Amt add Successfully...')
        return redirect('admin_share_percentage')
    context = {
        'share_percentage':share_percentage,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }
    return render(request,'homofix_app/AdminDashboard/SharePercentage/share_percentage.html',context)

def admin_share_percentage_update(request):
    if request.method == "POST":
        hod_share_percentage_id = request.POST.get('hod_share_percentage_id')
        share_amt = request.POST.get('share_amt')
        percentage_id = HodSharePercentage.objects.get(id=hod_share_percentage_id)
        percentage_id.percentage = share_amt
        percentage_id.save()
        messages.success(request,"Percentage updated successfully")
        return redirect('admin_share_percentage')

        
def admin_share_list(request):
    share = Share.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    for i in share:
        sub_ttl = i.task.booking.total_amount
        
        ttl = sub_ttl + i.task.booking.tax_amount
        
    context = {
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'share':share,
        'ttl':ttl
    }

    return render(request,'homofix_app/AdminDashboard/SharePercentage/list_of_share.html',context)


def admin_share_percentage_delete(request,id):
    share_percentage = HodSharePercentage.objects.get(id=id)
    share_percentage.delete()
    messages.success(request, "Share Percentage deleted successfully.")
    return redirect('admin_share_percentage')
def admin_customer_list(request):
    customer = Customer.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'customer':customer,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }
    return render(request,'homofix_app/AdminDashboard/Customer/customer_list.html',context)    

def admin_customer_edit(request,id):
    state_choices = STATE_CHOICES
    customer = Customer.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mob_no')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        area = request.POST.get('area')
        zipcode = request.POST.get('zipcode')
        customer.admin.first_name = first_name
        customer.admin.email = email
        customer.mobile = mobile
        customer.city = city
        customer.state = state
        customer.area = area
        if zipcode:
            customer.zipcode = zipcode
        
        customer.address = address
        customer.save()
        messages.success(request,'Customer Updated Successfully..')
        return redirect('admin_customer_edit', id=customer.id)
         
    context = {
        'customer':customer,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'state_choices':state_choices,

    }

    return render(request,'homofix_app/AdminDashboard/Customer/edit_customer.html',context)    

def admin_customer_history(request,id):
    customer = Customer.objects.get(id=id)
    
    booking = Booking.objects.filter(customer_id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    payment = Payment.objects.filter(booking_id=id)
   
    context = {
        'customer':customer,
        'booking':booking,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'payment':payment
    }


    return render(request,'homofix_app/AdminDashboard/History/CustomerHistory/customer_history.html',context)


# --------------------------- Customer Payment Details -----------------------------    

def admin_customer_payment(request):
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    payment = Payment.objects.all()
    context = {
        'payment':payment,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
    }

    return render(request,'homofix_app/AdminDashboard/CustomerPayment/list_of_payment.html',context)



def admin_reset_psw(request):
   
    id = request.user.id
    print("iddd",id)
    if request.method == "POST":
        old_psw = request.POST.get('old_psw')
        new_psw = request.POST.get('new_psw')
        confirm_psw = request.POST.get('confirm_psw')
        # id = request.user.id
        user = CustomUser.objects.get(id=id)
        
        if old_psw and new_psw:
            if user.check_password(old_psw):
                if new_psw == confirm_psw:
                    if old_psw == new_psw:
                        messages.error(request, 'New password must be different from the old password')
                        return redirect('admin_reset_psw')
                    else:
                        user.set_password(new_psw)
                        user.save()
                        messages.success(request,'Password successfully changed')
                        return redirect('admin_reset_psw')
                else:
                    messages.error(request, 'Passwords do not match')
                    return redirect('admin_reset_psw')
            else:
                messages.error(request, 'Old password is incorrect')
                return redirect('admin_reset_psw')
    return render(request, 'homofix_app/Authentication/reset_psw.html')
        

        # if old_psw and new_psw:
        #     if user.check_password(old_psw):
        #         if new_psw == confirm_psw:

        #             user.set_password(new_psw)
        #             messages.success(request,'success: password changed')
        #             return redirect('admin_reset_psw')
        #             # print("success: password changed")
        #         else:
        #             messages.error(request,'password not match')
        #             return redirect('admin_reset_psw')
        #             # print("password not match")
        #     else:
        #         messages.error(request,'old password does not match')
        #         return redirect('admin_reset_psw')
                # print("error: old password does not match")
    # return render(request,'homofix_app/Authentication/reset_psw.html')


# ------------------------------- Withdraw Request ----------------------     

def admin_withdraw_request(request):
    withdraw_req = WithdrawRequest.objects.all()
    context = {
        'withdraw_req':withdraw_req
    }
    return render(request,'homofix_app/AdminDashboard/Withdraw/withdraw_request.html',context)



    
def expert_cancel_withraw_request(request,withdraw_id):
    withdraw_req=WithdrawRequest.objects.get(id=withdraw_id)
    withdraw_req.status="Cancel"
    withdraw_req.save()
    return HttpResponseRedirect(reverse("admin_withdraw_request"))

    
def expert_accept_withraw_request(request,withdraw_id):
    withdraw_req=WithdrawRequest.objects.get(id=withdraw_id)
    withdraw_req.status="Accept"
    withdraw_req.save()
    return HttpResponseRedirect(reverse("admin_withdraw_request"))



# ------------------------------------------- Recharge ---------------- 

def recharge(request):
    
    
    recharge = RechargeHistory.objects.all()
    context = {
        'recharge':recharge
    }
    return render(request,'homofix_app/AdminDashboard/Recharge/list_of_recharge.html',context)



# ------------------------------ Attendance ------------------------ 

def attendence(request,id):

    attendence = Attendance.objects.filter(support_id=id)
    context = {
        'attendence':attendence
    }
    return render(request,'homofix_app/AdminDashboard/Attendence/list_of_attendence.html',context)


# ------------------------------ Coupon ------------------------ 


def coupon(request):
    
    
    coupon = Coupon.objects.all()
    context = {
        'coupon':coupon
    }
    return render(request,'homofix_app/AdminDashboard/Coupon/coupon.html',context)

def coupon_save(request):
    if request.method == "POST":
        code = request.POST.get('code') 
        discount_amt = request.POST.get('discount_amt') 
        validity_period = request.POST.get('validity_period') 

        code = Coupon.objects.create(code=code,discount_amount=discount_amt,validity_period=validity_period)
        code.save()
        messages.success(request,'Coupon Code Add Succesfull')
        return redirect('coupon')


def coupon_update(request):
    if request.method == "POST":
        pass



def add_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        feature_img = request.FILES.get('feature_img')
        content = request.POST.get('content')
        print("feature img",feature_img)
        blog = Blog.objects.create(title=title,feature_img=feature_img,content=content)
        messages.success(request,'Blog Add Successfully')
        return redirect('view_blog')
        
    return render(request,'homofix_app/AdminDashboard/Blog/add_blog.html')


def edit_blog(request,id):
    blog = Blog.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'blog':blog,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count
    }

    return render(request,'homofix_app/AdminDashboard/Blog/edit_blog.html',context)


def blog_update(request):

    if request.method == "POST":
        blog_id = request.POST.get('blog_id')
        title = request.POST.get('title')
        feature_img = request.POST.get('feature_img')
        content = request.POST.get('content')
        blog = Blog.objects.get(id=blog_id)
        blog.title = title
        if feature_img: 
            blog.feature_img = feature_img
        blog.content = content
        blog.save()
        messages.success(request,"Blog Updated are successfully")
        return redirect('view_blog')
        

def view_blog(request):
    blog = Blog.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    
    context = {
        'blog':blog,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count

    }

    return render(request,'homofix_app/AdminDashboard/Blog/view_blog.html',context)


def delete_blog(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request,"Blog Delete Successfully")
    return redirect('view_blog')








def ViewPDF(request,booking_id):
    
    import os
        
    if os.path.exists('last_invoice_number.txt'):
        with open('last_invoice_number.txt', 'r') as f:
            last_invoice_number = int(f.read().strip())
    else:
        last_invoice_number = 0

# Increment the last invoice number
    new_invoice_number = f'INV-{last_invoice_number+1:03d}'

# Save the new invoice number to the file
    with open('last_invoice_number.txt', 'w') as f:
        f.write(str(last_invoice_number+1))

# Print the new invoice number
    print("newwwwww",new_invoice_number)
    # print("ggggg")
    book_id = Booking.objects.get(id=booking_id)

    filename  = f"invoice_{book_id.order_id}.pdf"
    my_path = os.path.join(settings.MEDIA_ROOT, filename)
    # my_path = f"F:\\Homofix\\v75\\invoice_{book_id.order_id}.pdf"
    print("my path",my_path)
    # filename = f"invoice_{instance.order_id}.pdf"
    doc = SimpleDocTemplate(my_path, pagesize=letter,topMargin=0)

    
    # Add the title to the document
    para_style2 = ParagraphStyle(
    'title',
    fontSize=18,
    leading=20,
    alignment=TA_CENTER,  # align text to the left
    textColor=colors.black,
    spaceBefore=0,  # no space before the paragraph
    spaceAfter=12,
)

    
    title = Paragraph('LIST OF ITEM', para_style2)
    addon_title = Paragraph('LIST OF Addon', para_style2)
    inv = Paragraph('Invoice',para_style2)
    title.spaceBefore = 0  # set spaceBefore to zero
    addon_title.spaceBefore = 0  # set spaceBefore to zero
     # Create the table for bill to information
    bookingid=Booking.objects.get(id=booking_id)
   
    bill_to_data = [    ['Bill To:', bookingid.customer.admin.first_name],
        ['Address:', bookingid.customer.address],     
        ['Mobile:', f'+91{bookingid.customer.mobile}' ],
        ['Email:', bookingid.customer.admin.email],
    ]
    bill_to_table = Table(bill_to_data, colWidths=[150, None], hAlign='LEFT')
    


# Apply the bill to table style
    # bill_to_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])

    bill_to_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    # ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    
    ('LINEAFTER', (1, 0), (1, -1), 0.5, colors.black),
])

    bill_to_table.setStyle(bill_to_style)

    # Get the last invoice number from a file
    
# Create the table for invoice details
    invoice_data = [    ['Invoice No:', 'INV-001'],
        ['Invoice Date:', '18-Apr-2023'],
        # ['Due Date:', '30-Apr-2023'],
    ]

    invoice_table = Table(invoice_data, colWidths=[150, None], hAlign='LEFT')



    # Apply the invoice table style
    # invoice_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
    invoice_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
])

    invoice_table.setStyle(invoice_style)
    
    nested_table_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('BOX', (0, 0), (-1, -1), 1, colors.black),
])

    # Create the nested table with two columns and one row
    nested_table_data = [[bill_to_table, invoice_table]]
    nested_table = Table(nested_table_data, colWidths=[250, 250])
    nested_table.setStyle(nested_table_style)


    # Define the table data
    
    data = [['Product Name', 'Qty','RATE','TAX','AMOUNT'],]
    addon = [['Addon Name', 'Qty','RATE','TAX','AMOUNT'],]
    bookingProd=BookingProduct.objects.filter(booking=booking_id)
    adon = Addon.objects.filter(booking_prod_id__booking=booking_id)
    # stu = Booking.objects.all()
    for bookingprod in bookingProd:

        price = 0
        if bookingprod.product.selling_price != None:
            price = bookingprod.product.selling_price
        else:
            price = bookingprod.product.price
        
        data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',f'{bookingprod.quantity*price*1.18:.2f}'])
        # data.append([bookingprod.product.name, bookingprod.quantity,price,'18%',bookingprod.quantity*price*1.18])
        for i in adon:
            if i.spare_parts_id.product == bookingprod.product:
                # addon.append([i.spare_parts_id.spare_part,i.quantity,i.spare_parts_id.price,'18%',i.quantity*i.spare_parts_id.price*1.18])
                addon.append([i.spare_parts_id.spare_part, i.quantity, i.spare_parts_id.price, '18%', f'{i.quantity * i.spare_parts_id.price * 1.18:.2f}'])


        # if i.spare_parts_id.product ==  bookingprod.product:
        #     addon.append([i.spare_parts_id.spare_part])
            
        
#     data.append(['Ac Repairing', '2','100','18%','200'])
        

    # Create the table
    # col_widths = [100, 100]
    col_widths = [270, 30, 75, 50, 70]
    table = Table(data,colWidths=col_widths)
    addon_col_widths = [270, 30, 75, 50, 70]
    addontable = Table(addon,colWidths=addon_col_widths)

    # Apply the table style
    style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    table.setStyle(style)
    
    addonstyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        # ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        # ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ])
    addontable.setStyle(addonstyle)
    

    # Define the paragraph style
    para_style = ParagraphStyle(
        'title',
        fontSize=18,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=12,
    )
    
    
    logo_path = os.path.join(settings.MEDIA_ROOT, 'LOGO2.jpeg')

    
    
    logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
    logo.hAlign = 'LEFT'



    
    
    # Create the table for invoice totals
    booking = Booking.objects.get(id=booking_id)
    tax_rate = 0.18
    total_price = total_price = booking.total_amount
    print("ttoaalll",total_price)
    gst = int(total_price * 18)/100
    total = total_price+gst
    # print("gsstttt",gst)

    invoice_totals_data = [    ['Subtotal:', f'{total_price:.2f}'],
        ['CGST @9%:', f'{gst/2:.2f}'],
        ['SGST @9%:', f'{gst/2:.2f}'],
        ['Total:', f'{total:.2f}'],
    ]

    invoice_totals_table = Table(invoice_totals_data, colWidths=[90, None], hAlign='RIGHT')

# Apply the invoice totals table style
    # invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),])
    invoice_totals_style = TableStyle([    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),    ('FONTSIZE', (0, 0), (-1, -1), 11),    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),    ('LINEABOVE', (0, 3), (-1, 3), 1, colors.black),('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),])
    invoice_totals_table.setStyle(invoice_totals_style)


    # Create the table for company information
    company_data = [        [''],  # Add an empty row before the company information
        [f'{"Homofix Technologies PVT Ltd":^65}'],
        # [''],
        [f'{"Corporate Office: 2nd Floor, WP-501-D, Unit 209, Shiv Market, Wazirpur Village ,":^50}'],
        [f'{"Ashok Vihar, New Delhi, Central Delhi, Delhi, 110052":^90}'],
        [f'{"Regd Office: 5139, Awas Vikas 3, Kalyanpur,Kanpur,Uttar Pradesh, India,208017":^50}'],
        [f'{"GSTIN:07AAGCH4863F1Z1":^110}'],

        # ['Ashok Vihar Delhi,New Delhi 110052'],
        # [ '+1 (555) 987-6543'],
        # ['info@abccorp.com'],
    ]
    

    # company_table = Table(company_data, colWidths=[90, None])
    company_table = Table(company_data, colWidths=[doc.width, 0])

    # Apply the company table style
 
    # Apply the company table style
    company_style = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),  # Add line below style to the first row
    ('FONTSIZE', (0, 1), (-1, -1), 20),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (0, 0), 6),  # Add top padding to the first cell of the first row
    ('LEFTPADDING', (0, 0), (0, 0), 50),  # Add left padding to the first cell of the first row
    ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Align the first cell of the first row to the center
    # ('TEXTCOLOR', (0, 0), (-1, -1), colors.blue),
    # ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid style to all cells
    ('FONTSIZE', (0, 2), (-1, 2), 12),
    ('FONTSIZE', (0, 3), (-1, 3), 12),
    ('TOPPADDING', (0, 3), (-1, 3), -8),
    ('FONTSIZE', (0, 4), (-1, 4), 12),
    ('FONTSIZE', (0, 5), (-1, 5), 12),
    ('TOPPADDING', (0, 5), (-1, 5), -6),
    # ('LINEBELOW', (-1, -1), (-1, -1), 1, colors.black)  # Add line below style to the last row
])
    company_table.setStyle(company_style)

   
    # doc = SimpleDocTemplate(f'invoice{}.pdf', topMargin=0)

    doc.build([inv,logo, nested_table, Spacer(1, 0.*inch),title, table,Spacer(1, 0.1*inch),addon_title,addontable, Spacer(1, 0.5*inch), invoice_totals_table, Spacer(1, 0.5*inch), company_table])
    import os
    if os.path.exists(my_path):
        with open(my_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
            return response
    # else:
    #     return HttpResponse("The requested file does not exist.")

    return HttpResponse("Invoice generated successfully")        