from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import CustomUser,Category,Technician,Product,Addons,Support,FAQ,Booking,Task,STATE_CHOICES
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


# @login_required
def admin_dashboard(request):
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    
    return render(request,'homofix_app/AdminDashboard/dashboard.html',{'booking_count':booking_count,'new_expert_count':new_expert_count})


def admin_profile(request):

    return render(request,'homofix_app/AdminDashboard/profile.html')


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
    return render(request,'homofix_app/AdminDashboard/Category/category.html',{'category':category,'new_expert_count':new_expert_count})

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

def technician(request):
    category = Category.objects.all()
    technician = Technician.objects.filter(status="Active")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
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

    return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician,'new_expert_count':new_expert_count,'booking_count':booking_count})


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
        
        elif status == 'New':
            technician.status = 'New'

        else:
            technician.status = 'Active'

        technician.rating=rating
        technician.serving_area=serving_area
        technician.highest_qualification=highest_qualification
        technician.state=state
        technician.city=city
        # technician.joining_date=date_of_joining
        if date_of_joining:
            technician.joining_date =date_of_joining
        if application_form != None:
            technician.application_form=application_form
        

        cat = Category.objects.get(id=category_id)

        technician.category=cat

        technician.admin.save()
        technician.save()
        messages.success(request,'updated sucessfully')
        return redirect('technician_edit_profile',id=technician.id)
        # return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})
        # return redirect('technician_edit_profile',{'technician_id': technician_id})
    return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category,'state_choices':state_choices,'new_expert_count':new_expert_count,'booking_count':booking_count })


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





def product(request):

    product = Product.objects.all()
    category = Category.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    if request.method == "POST":       
        
        product_pic = request.FILES.get('product_pic')
        product_name = request.POST.get('product_name')
        product_title = request.POST.get('product_title')
        price = request.POST.get('price')
        warranty = request.POST.get('warranty')
        description = request.POST.get('desc')
        warranty_desc = request.POST.get('warranty_desc')
        category_id = request.POST.get('category_id')
       
        
        
        if Product.objects.filter(name = product_name).exists():
            # return JsonResponse({'status': 'error', 'message': 'Product is already Taken'})
            messages.warning(request,'Product is already Taken')
            return redirect('product')
            
        cat = Category.objects.get(id=category_id)
        product = Product.objects.create(product_pic=product_pic,name=product_name,product_title=product_title,category=cat,price=price,warranty=warranty,warranty_desc=warranty_desc,description=description)
        messages.success(request,'Product Add Successfully')
        product.save()
        return redirect('product')
        
        # return JsonResponse({'status':'Save'})
    return render(request,'homofix_app/AdminDashboard/Product/product.html',{'product':product,'category':category,'new_expert_count':new_expert_count,'booking_count':booking_count})


def update_product(request):
    if request.method == "POST":
        
        product_id = request.POST.get('product_id')
        category_id = request.POST.get('category_id')
        product_pic = request.FILES.get('product_pic')

        product_title = request.POST.get('product_title')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        warranty = request.POST.get('warranty')
        description = request.POST.get('description')

        print("description",description)

        
        cat = Category.objects.get(id=category_id)
        product = Product.objects.get(id=product_id)
        if product_pic != None:
            product.product_pic = product_pic
        product.category = cat
        product.product_title = product_title
        product.name = product_name
        product.price = price
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
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        desc = request.POST.get('desc')

        prod = Product.objects.get(id=product_id)

        ad = Addons.objects.create(product=prod,description=desc)
        prod.save()
        messages.success(request,'Addon Add Successfully')
        return redirect('addons')
        

    return render(request,'homofix_app/AdminDashboard/Addons/addon.html',{'addons':addons,'product':product,'new_expert_count':new_expert_count,'booking_count':booking_count})



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
    return render(request,'homofix_app/AdminDashboard/Support/support.html',{'suppt':suppt,'new_expert_count':new_expert_count,'booking_count':booking_count})

def add_support(request):
    if request.method == "POST":
        
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

      
        if CustomUser.objects.filter(username = username).exists():
            messages.error(request,'Username is already Taken')
            return redirect('admin_support')
            
        user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type='3')
        
        user.save()
        messages.success(request,'Support Register Successfully')
        return redirect('admin_support')
        
        

    return redirect('admin_support')


def support_profile(request,id):
    support = Support.objects.get(id=id)
    new_expert_count = Technician.objects.filter(status="New").count()
    return render(request,'homofix_app/AdminDashboard/Support/edit_profile.html',{'support':support,'new_expert_count':new_expert_count})



def support_update_profile(request):
    if request.method == "POST":
        support_id = request.POST.get('support_id')
       
        profile_pic = request.FILES.get('profile_pic') 
        username = request.POST.get('username')
        email = request.POST.get('email')
        mob_no = request.POST.get('mob_no')
        address = request.POST.get('address')
        date_of_joining = request.POST.get('date_of_joining')
        status = request.POST.get('status')
        application_form = request.FILES.get('application_form')
        support = Support.objects.get(id=support_id)

       
        support.admin.username =username 
        support.admin.email =email
        if profile_pic != None:
            support.profile_pic =profile_pic
        
        if application_form != None:
            support.application_form =application_form


        support.address =address 
        support.mobile =mob_no 
        if date_of_joining:

            support.joining_date =date_of_joining 

        if status == 'Deactivate':
            support.status = "Deactivate"
            
        elif status == 'Hold':
            support.status = 'Hold'
        else:
            support.status = 'Active'

        support.save()
        messages.success(request,'Support Updated Succesffully')
        return HttpResponseRedirect(reverse("support_profile",args=[support_id]))



def delete_support(request,id):
    support = Support.objects.get(id=id)
    user = support.admin
    support.delete()
    user.delete()
    messages.success(request, "Support deleted successfully.")
    return redirect('admin_support')
    
        


# ------------------------------- FAQS ------------------------------        



def add_faq(request):
    product = Product.objects.all()
    faqs = FAQ.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
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
        'booking_count':booking_count
    }

    return render(request,'homofix_app/AdminDashboard/Faqs/faqs.html',context)


def booking_list(request):
    booking_count = Booking.objects.filter(status = "New").count()
    booking = Booking.objects.all()
    
    technicians = Technician.objects.all()
    tasks = Task.objects.all()
    new_expert_count = Technician.objects.filter(status="New").count()
    context = {
    'booking':booking,
    'technicians':technicians,
    'tasks':tasks,
    'new_expert_count':new_expert_count,
    'booking_count':booking_count
    
    
    
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
    context = {
        'task':task,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count,
        
    }
    return render(request,'homofix_app/AdminDashboard/Booking_list/task.html',context)    


def Listofcancel(request):
    booking = Booking.objects.filter(status="cancelled")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    context = {
        'booking':booking,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count
    }
    return render(request,'homofix_app/AdminDashboard/Booking_list/cancel_booking.html',context)    


def ListofNewExpert(request):
    category = Category.objects.all()
    technician = Technician.objects.filter(status="New")
    new_expert_count = Technician.objects.filter(status="New").count()
    booking_count = Booking.objects.filter(status = "New").count()
    
    context = {
        'category' :category,
        'technician':technician,
        'new_expert_count':new_expert_count,
        'booking_count':booking_count
    }
    return render(request,'homofix_app/AdminDashboard/Notification/New_expert.html',context)