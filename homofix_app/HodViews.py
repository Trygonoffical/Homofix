from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import CustomUser,Category,Technician,Product,Addons,Support,FAQ,Booking,Task,STATE_CHOICES,SubCategory,Rebooking,ContactUs,JobEnquiry,HodSharePercentage,Customer,Share
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import random
from django.contrib.auth.models import Permission



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


def admin_update_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        if CustomUser.objects.filter(username = username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
          
        id = request.user.id
        user = CustomUser.objects.get(id=id)
        user.username = username
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
   
    category = Category.objects.all()
    subcategories = technician.subcategories.all()
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
        if city:
            city = city.lower()
        technician.city=city
        # technician.joining_date=date_of_joining
        if date_of_joining:
            technician.joining_date =date_of_joining
        if application_form != None:
            technician.application_form=application_form
        

        # cat = Category.objects.get(id=category_id)
        if subcategory_id:
            subcategories = SubCategory.objects.filter(id__in=subcategory_id)
            technician.subcategories.set(subcategories)
           

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
    context = {
        'task':task,
        'rebooking':rebooking
    }
   
    return render(request,'homofix_app/AdminDashboard/History/task_history.html',context)
   

def product(request):
    product = Product.objects.all()
    category = Category.objects.all()
    subcategory = SubCategory.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_pic = request.FILES.get("product_pic")
        product_name = request.POST.get("product_name")
        product_title = request.POST.get("product_title")
        price = request.POST.get("price")
        discount_amt = request.POST.get("discount_amt")
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
        'customer_count':customer_count
    }
    return render(request, "homofix_app/AdminDashboard/Product/product.html", context)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(Category_id=category_id)
    data = list(subcategories.values('id', 'name'))
    return JsonResponse(data, safe=False)




def get_products(request):
    subcategory_id = request.GET.get('subcategory_id')
    if subcategory_id:
        subcategory_id = int(subcategory_id)
        products = Product.objects.filter(subcategory_id=subcategory_id)
        data = [{'id': product.id,'price': product.price, 'name': product.name} for product in products]
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
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        warranty = request.POST.get('warranty')
        description = request.POST.get('description')

        print("description",description)

        
        # cat = Category.objects.get(id=category_id)
        subcat = SubCategory.objects.get(id=subcategory_id)
        product = Product.objects.get(id=product_id)
        if product_pic != None:
            product.product_pic = product_pic
        product.subcategory = subcat
        product.product_title = product_title
        product.name = product_name
        product.price = price
        product.dis_amt = discount_price
        product.warranty = warranty
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
    addons = Addons.objects.all()
    product = Product.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        desc = request.POST.get('desc')

        prod = Product.objects.get(id=product_id)

        ad = Addons.objects.create(product=prod,description=desc)
        prod.save()
        messages.success(request,'Addon Add Successfully')
        return redirect('addons')
        

    return render(request,'homofix_app/AdminDashboard/Addons/addon.html',{'addons':addons,'product':product,'new_expert_count':new_expert_count,'booking_count':booking_count,'rebooking_count':rebooking_count,'customer_count':customer_count})



def update_addons(request):

    if request.method == "POST":
        product_id  = request.POST.get('product_id')
        addon_id  = request.POST.get('addon_id')
        description  = request.POST.get('description')

        print("sssssssssssssssssssssss",product_id)
        product = Product.objects.get(id=product_id)
        addons = Addons.objects.get(id=addon_id)
        
        addons.product = product
        addons.description =description
        print("sssssssssssssssssssssss",product_id)
        addons.save()
        messages.success(request,'Addons Updated Successfully')
        return redirect('addons')

    

def delete_addons(request,id):

    addon = Addons.objects.get(id=id)
    addon.delete()
    messages.success(request, "Addon deleted successfully.")
    return redirect('addons')




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


def support_update_profile(request):
    if request.method == "POST":
        support_id = request.POST.get('support_id')
       
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

        support = Support.objects.get(id=support_id)
        
        
        if profile_pic:
            support.profile_pic = profile_pic
        
        if application_form:
            support.application_form=application_form

        if document_form:
            support.document_form=document_form

        
        # if application_form:
        #     application_form_str = ','.join(str(file) for file in application_form)
        #     support.application_form = application_form_str
        print("helooooo",support.admin.first_name) 
        # support.admin.last_name = lastname 
        # support.admin.username = username 
        # support.admin.email = email
        support.admin.first_name = firstname 
        support.address = address 
        support.permanent_address = permanent_address 
        support.father_name = father_name 
        support.marital_status = marital_status 
        support.d_o_b = dob 
        support.mobile = mob_no 


        support.can_new_booking = True if can_new_booking == 'on' else False
        support.can_cancel_booking = True if can_cancel_booking == 'on' else False
        support.can_rebooking = True if can_rebooking == 'on' else False
        support.can_assign_task = True if can_assign_task == 'on' else False
        support.can_expert_create = True if can_new_expert == 'on' else False
        support.can_contact_us_enquiry = True if can_customer_enquiry == 'on' else False
        support.can_job_enquiry = True if can_job_enquiry == 'on' else False


        if date_of_joining:
            support.joining_date = date_of_joining 

        if status == 'Deactivate':
            support.status = "Deactivate"
        elif status == 'Hold':
            support.status = 'Hold'
        else:
            support.status = 'Active'

        
        support.save()
        messages.success(request, 'Support Updated Succesffully')
        return HttpResponseRedirect(reverse("support_profile",args=[support_id]))


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
        'customer_count':customer_count
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
    
    technicians = Technician.objects.all()
    tasks = Task.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
    'booking':booking,
    'technicians':technicians,
    'tasks':tasks,
    'new_expert_count':new_expert_count,
    'booking_count':booking_count,
    'rebooking_count':rebooking_count,
    'customer_count':customer_count
    
    
    
   }
    
    
    
    return render(request,'homofix_app/AdminDashboard/Booking_list/booking.html',context)    




def admin_reschedule(request):
    if request.method == "POST":

        booking_id=request.POST.get('booking_id')
        booking_date=request.POST.get('booking_date')
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

def admin_share_list(request):
    share = Share.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    rebooking_count = Rebooking.objects.all().count()
    customer_count = Customer.objects.all().count()
    context = {
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        'rebooking_count':rebooking_count,
        'customer_count':customer_count,
        'share':share
    }

    return render(request,'homofix_app/AdminDashboard/SharePercentage/list_of_share.html',context)
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
    print("customerr id",customer)
    booking = Booking.objects.filter(customer_id=id)
    print("helloooo",booking)
    context = {
        'customer':customer,
        'booking':booking
    }


    return render(request,'homofix_app/AdminDashboard/History/CustomerHistory/customer_history.html',context)