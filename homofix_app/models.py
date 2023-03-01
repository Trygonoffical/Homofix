from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import generate_ref_code,generate_expert_code,generate_support_code,generate_order_code
from ckeditor.fields import RichTextField
import os
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=(('1',"HOD"),('2',"Technician"),('3',"Support"),('4',"Customer"))
    user_type=models.CharField(default='1',choices=user_type_data,max_length=10)



class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.admin.username
    

class Category(models.Model):    
    
    category_name = models.CharField(max_length=50)
    created_at=models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    objects=models.Manager()

    def __str__(self):
        return self.category_name
    

    

status = (
    ('Active','Active'),
    ('Deactivate','Deactivate'),
    ('Hold','Hold'),
)


class Technician(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'Technician', null= True, blank=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    expert_id = models.CharField(max_length=12,blank=True)
    # user_id = models.CharField(max_length=12,blank=True)
    Father_name = models.CharField(max_length=100,null=True,blank=True)
    present_address = models.TextField(null=True,blank=True)
    permanent_address = models.TextField(null=True,blank=True)
    Id_Proof = models.CharField(max_length=100,null=True,blank=True)
    id_type = models.CharField(max_length=100,null=True,blank=True)
    id_proof_document = models.ImageField(upload_to='ID Proof',null=True,blank=True)
    application_form = models.ImageField(upload_to='Expert/Application Form',null=True,blank=True)
    expert_in = models.CharField(max_length=50,null=True,blank=True)
    serving_area = models.CharField(max_length=100,null=True,blank=True)
    highest_qualification = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(choices=status,max_length=50,default='Active')
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    joining_date = models.DateField(null=True,blank=True)
    objects=models.Manager()

    def save(self, *args, **kwargs):
        if not self.expert_id:
            self.expert_id = generate_expert_code()
        # if not self.user_id:
        #     self.user_id = generate_ref_code()
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if not self.expert_id:
    #         self.expert_id = generate_expert_code()
    #     super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     if self.user_id == "":
    #         user_id = (generate_ref_code())
    #         self.user_id = user_id
    #     super().save(*args, **kwargs)
   
   
    def delete(self, *args, **kwargs):
        if self.profile_pic:
            if os.path.isfile(self.profile_pic.path):
                os.remove(self.profile_pic.path)
        super().delete(*args, **kwargs)


class Support(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Support', null=True, blank=True)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=50)
    status = models.CharField(choices=status, max_length=50, default='Active')
    bookings = models.ManyToManyField('Booking', blank=True, related_name='supported_by_staff')
    support_id = models.CharField(max_length=12,blank=True)
    joining_date = models.DateField(null=True,blank=True)
    application_form = models.ImageField(upload_to='Support/Application Form',null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.support_id:
            self.support_id = generate_support_code()
        # if not self.user_id:
        #     self.user_id = generate_ref_code()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.application_form:
            if os.path.isfile(self.application_form.path):
                os.remove(self.application_form.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.admin.username


class Customer(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.admin.username
    


class Product(models.Model):
    product_pic = models.ImageField(upload_to = 'Product Image')
    product_title = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    price = models.IntegerField()
    warranty = models.CharField(max_length=50,null=True,blank=True)
    warranty_desc = RichTextField(null=True,blank=True)
    description = RichTextField()
    created_at=models.DateField(auto_now_add=True)

   


class FAQ(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = RichTextField()


class Addons(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = RichTextField()
    created_at=models.DateField(auto_now_add=True)



class Booking(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('in_process', 'In Process'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_supported_by')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    order_id = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_code()
        # if not self.user_id:
        #     self.user_id = generate_ref_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.admin.username} - {self.product.name}"


class feedback(models.Model):
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)



class Task(models.Model):
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task for {self.booking.customer.admin.username} - {self.booking.product.name}"

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type=='1':
            AdminHOD.objects.create(admin=instance)
        if instance.user_type=='2':
            category = Category.objects.first()
            Technician.objects.create(admin=instance,category=category,present_address="")
        if instance.user_type=='3':
            
            Support.objects.create(admin=instance,address="")
        if instance.user_type=='4':
            
            Customer.objects.create(admin=instance,address="")



@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type=='1':
        instance.adminhod.save()
    if instance.user_type=='2':
        instance.technician.save() 
    if instance.user_type=='3':
        instance.support.save()
    if instance.user_type=='4':
        instance.customer.save()
   
    
