from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.decorators import login_required
from .models import CustomUser,Category,Technician,Product
from django.http import JsonResponse


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
        print("helooooo",category_name)
        
        
        if Category.objects.filter(category_name = category_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Category is already Taken'})
            
        category = Category.objects.create(category_name=category_name)
        # category.save()
        
        return JsonResponse({'status':'Save'})



def technician(request):
    category = Category.objects.all()
    technician = Technician.objects.all()
    if request.method == "POST":
        
        category_id = request.POST.get('category_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(category_id)

        ctg = Category.objects.get(id=category_id)
      
        if CustomUser.objects.filter(username = username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username is already Taken'})
            
        user = CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.technician.category = ctg
        user.save()
        if(user.is_active):
            return JsonResponse({'status':'Save'})
            
        else:
            return JsonResponse({'status':0})

    return render(request,'homofix_app/AdminDashboard/Technician/technician.html',{'category':category,'technician':technician})


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