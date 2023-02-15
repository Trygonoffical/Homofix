from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import CustomUser,Category,Technician,Product
from django.http import JsonResponse
from django.contrib import messages


# @login_required
def admin_dashboard(request):
    return render(request,'homofix_app/AdminDashboard/dashboard.html')


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
    return render(request,'homofix_app/AdminDashboard/Category/category.html',{'category':category})

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
            return redirect('technician')
            
        user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.technician.category = ctg
        user.save()
        messages.success(request,'Technician Register Successfully')
        # if(user.is_active):
        #     return JsonResponse({'status':'Save'})
            
        # else:
        #     return JsonResponse({'status':0})

    return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician})


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
    technician = Technician.objects.get(id=id)
    category = Category.objects.all()
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
        expert_in = request.POST.get('expert_in')
        serving_area = request.POST.get('serving_area')
        highest_qualification = request.POST.get('highest_qualification')
        state = request.POST.get('state')
        city = request.POST.get('city')
        status = request.POST.get('status')   

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

        technician.expert_in=expert_in
        technician.serving_area=serving_area
        technician.highest_qualification=highest_qualification
        technician.state=state
        technician.city=city


        cat = Category.objects.get(id=category_id)

        technician.category=cat

        technician.admin.save()
        technician.save()
        messages.success(request,'updated sucessfully')
        return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})
        # return redirect('technician_edit_profile',{'technician_id': technician_id})
    return render(request,'homofix_app/AdminDashboard/Technician/technician_profile.html',{'technician':technician,'category':category})


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

    if request.method == "POST":
        
        
        product_pic = request.FILES.get('product_pic')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        print(product_name,price,description,product_pic)
        
        
        if Product.objects.filter(name = product_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Product is already Taken'})
            

        product = Product.objects.create(product_pic=product_pic,name=product_name,price=price,description=description)
        product.save()
        
        return JsonResponse({'status':'Save'})
    return render(request,'homofix_app/AdminDashboard/Product/product.html',{'product':product})