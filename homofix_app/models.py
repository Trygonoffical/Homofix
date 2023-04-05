from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .utils import generate_ref_code,generate_expert_code,generate_support_code,generate_order_code
from ckeditor.fields import RichTextField
import os
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.db.models import Sum
from decimal import Decimal
import datetime


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
    
class SubCategory(models.Model):
    Category_id = models.ForeignKey(to=Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at=models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name
    
    

status = (
    ('Active','Active'),
    ('Inactive','Inactive'),
    ('New','New'),
    # ('Deactivate','Deactivate'),
    ('Hold','Hold'),
)

STATE_CHOICES = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal', 'Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnatka', 'Karnatka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttarakhand', 'Uttarakhand'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('West Bengal', 'West Bengal'),
        ('Delhi', 'Delhi'),
        # add more choices as needed
    )


class Support(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='Support', null=True, blank=True)
    address = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=50,null=True,blank=True)
    father_name = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=50,null=True,blank=True)
    d_o_b = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(choices=status, max_length=50, default='Active')
    bookings = models.ManyToManyField('Booking', blank=True, related_name='supported_by_staff')
    support_id = models.CharField(max_length=12,blank=True)
    joining_date = models.DateField(null=True,blank=True)
    application_form = models.FileField(upload_to='Support/Application Form',null=True,blank=True)
    document_form = models.FileField(upload_to='Support/Document Form',null=True,blank=True)
    can_assign_task = models.BooleanField(default=False)
    can_new_booking = models.BooleanField(default=False)
    can_cancel_booking = models.BooleanField(default=False)
    can_rebooking = models.BooleanField(default=False)
    can_expert_create = models.BooleanField(default=False)
    can_contact_us_enquiry = models.BooleanField(default=False)
    can_job_enquiry = models.BooleanField(default=False)

   

    def save(self, *args, **kwargs):
        if not self.support_id:
            last_support = Support.objects.order_by('-id').first()
            if last_support and '-' in last_support.support_id:
                last_id = int(last_support.support_id.split('-')[1])
            else:
                last_id = 2300
            new_id = last_id + 1
            self.support_id = f'HS-{new_id:03}'
        super().save(*args, **kwargs)


    def __str__(self):
        return self.admin.username



class Technician(models.Model):
   
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    subcategories = models.ManyToManyField(SubCategory, blank=True)
    profile_pic = models.ImageField(upload_to = 'Technician', null= True, blank=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    # expert_id = models.CharField(max_length=12,blank=True)
    expert_id = models.CharField(max_length=12, blank=True)

    # user_id = models.CharField(max_length=12,blank=True)
    Father_name = models.CharField(max_length=100,null=True,blank=True)
    present_address = models.TextField(null=True,blank=True)
    permanent_address = models.TextField(null=True,blank=True)
    Id_Proof = models.CharField(max_length=100,null=True,blank=True)
    id_type = models.CharField(max_length=100,null=True,blank=True)
    id_proof_document = models.ImageField(upload_to='ID Proof',null=True,blank=True)
    application_form = models.ImageField(upload_to='Expert/Application Form',null=True,blank=True)
    rating = models.CharField(max_length=50,null=True,blank=True)
    serving_area = models.CharField(max_length=100,null=True,blank=True)
    highest_qualification = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True,choices=STATE_CHOICES)
    city = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(choices=status,max_length=50,default='Active')
    # status_choice = models.CharField(choices=STATUS_CHOICES,max_length=50,default='New')
    supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    joining_date = models.DateField(null=True,blank=True)
    objects=models.Manager()


    def save(self, *args, **kwargs):
        if not self.expert_id:
            last_technician = Technician.objects.order_by('-id').first()
            if last_technician:
                last_id = int(last_technician.expert_id.split('-')[1])
            else:
                last_id = 0
            new_id = last_id + 1
            self.expert_id = f'HE-{new_id:03}'
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

    def __str__(self):
        return str(self.expert_id)
 


class Customer(models.Model):
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=50)
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True,choices=STATE_CHOICES)
    area = models.CharField(max_length=50,null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.admin.username
    


class Product(models.Model):
    product_pic = models.ImageField(upload_to = 'Product Image')
    product_title = models.CharField(max_length=50,null=True,blank=True)
    name = models.CharField(max_length=50)
    # category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    price = models.IntegerField()
    dis_amt = models.IntegerField(null=True,blank=True)
    warranty = models.CharField(max_length=50,null=True,blank=True)
    warranty_desc = RichTextField(null=True,blank=True)
    description = RichTextField()
    created_at=models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name
    

  

class FAQ(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = RichTextField()





class Booking(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Inprocess', 'Inprocess'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('Assign', 'Assign'),
        ('Proceed', 'Proceed'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='bookings', through='BookingProduct')
    booking_date = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings_supported_by')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    state = models.CharField(max_length=100,null=True,blank=True,choices=STATE_CHOICES)
    city = models.CharField(max_length=100,null=True,blank=True)
    area = models.CharField(max_length=100,null=True,blank=True)
    zip_code = models.CharField(max_length=10,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True) 
    order_id = models.CharField(max_length=9, unique=True, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.order_id:
            today = datetime.datetime.now()
            year_month = today.strftime('%Y%m')
            last_order = Booking.objects.filter(order_id__startswith=year_month).order_by('-id').first()
            if last_order:
                last_id = int(last_order.order_id.split('-')[-1])
            else:
                last_id = 0
            new_id = last_id + 1
            self.order_id = f'{year_month}-{new_id:03}'
        super().save(*args, **kwargs)



    def __str__(self):
         return f"{self.customer.admin.username} - {self.booking_date}"
        

class BookingProduct(models.Model):
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  
    total_price = models.IntegerField()
    total_price_with_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Calculate the total price with tax
        total_price_with_tax = self.total_price * Decimal('1.18')
        # Set the total price with tax for this booking product
        self.total_price_with_tax = total_price_with_tax
        super(BookingProduct, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name
    
    # def total_price(self):
    #     return self.quantity * self.price
    
    # def multiply(self, *args, **kwargs):
    #     self.total_price = self.quantity * self.price
    #     return self.total_price
        
        # super().save(*args, **kwargs)


class SpareParts(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    spare_part = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    description = models.TextField()
    created_at=models.DateField(auto_now_add=True)



# class Addon(models.Model):
    
#     booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
#     # addon_product = models.ManyToManyField(AddonsProduct)
#     addon_product = models.ForeignKey(AddonsProduct,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     date = models.DateField(auto_now_add=True)
#     description = models.TextField(null=True,blank=True)


class Addon(models.Model):
    booking_prod_id = models.ForeignKey(BookingProduct,on_delete=models.CASCADE)
    addon_products = models.ForeignKey(SpareParts,on_delete=models.CASCADE)
    # addon_products = models.ManyToManyField(SpareParts,related_name='addons')
    quantity = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True,blank=True)


class HodSharePercentage(models.Model):
    percentage = models.IntegerField()
    date = models.DateField(auto_now_add=True,null=True,blank=True)



   
class TechnicianLocation(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE,null=True,blank=True)
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    # latitude = models.DecimalField(max_digits=9, decimal_places=6)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # timestamp = models.DateTimeField(auto_now_add=True)
class feedback(models.Model):
    Customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)



class Task(models.Model):

    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    supported_by = models.ForeignKey(Support, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assign')

    # def __str__(self):
    #     return f"Task for {self.booking.customer.admin.username} - {self.booking.product.name}"



# class Rebooking(models.Model):
#     STATUS_CHOICES = (
#         ('Assign', 'Assign'),
#         ('Inprocess', 'Inprocess'),
#         ('completed', 'Completed'),
       
#     )
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='rebookings')
#     # new_booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='original_bookings')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assign')
#     technician = models.ForeignKey(Technician, on_delete=models.CASCADE,null=True,blank=True)
#     booking_date = models.DateTimeField(null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
        
#         self.booking.status = 'Assign'
#         self.booking.save()

#         super().save(*args, **kwargs)


class Share(models.Model):
    # booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    hod_share_percentage = models.ForeignKey(HodSharePercentage, on_delete=models.CASCADE)
    technician_share = models.IntegerField(default=0)
    hod_share = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True,null=True,blank=True)



class Wallet(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    total_share = models.IntegerField(default=0)

    def add_bonus(self, bonus_amount):
        self.total_share += bonus_amount
        self.save()

    def deduct_amount(self, amount):
        self.total_share -= amount
        self.save()

    def __str__(self):
        return self.technician.admin.username
    

class WalletHistory(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('bonus', 'Bonus'),
        ('deduction', 'Deduction'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.IntegerField()
    description = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.wallet.technician.admin.username)
    


class Rebooking(models.Model):
    STATUS_CHOICES = (
        ('Assign', 'Assign'),
        ('Inprocess', 'Inprocess'),
        ('completed', 'Completed'),
    )
    
    booking_product = models.ForeignKey(BookingProduct, on_delete=models.CASCADE, related_name='rebookings')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assign')
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.technician:
            # get the technician assigned to the original Task
            try:
                task = Task.objects.get(booking=self.booking_product.booking, status='Assign')
                self.technician = task.technician
            except Task.DoesNotExist:
                pass
        super(Rebooking, self).save(*args, **kwargs)


class ContactUs(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class JobEnquiry(models.Model):
    name = models.CharField(max_length=50)    
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='Job/Job Enquiry Form',null=True,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('Online', 'Online'),
        ('Cash On Services', 'Cash On Services'),
        ('Qr', 'Qr'),
    )
    booking_id = models.ForeignKey(Booking,on_delete=models.CASCADE)  
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    # total_price_with_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True,null=True,blank=True)

    # def save(self, *args, **kwargs):
    #     # Get the booking associated with this payment
    #     booking = self.booking_id
    #     # Calculate the total price with tax
    #     total_price_with_tax = booking.bookingproduct_set.aggregate(
    #         total=Coalesce(Sum('total_price'), 0) * Decimal('1.18')
    #     )['total']
    #     # Set the total price with tax for this payment
    #     self.total_price_with_tax = total_price_with_tax
    #     super(Payment, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.booking_id)
    
class Kyc(models.Model):
    technician_id = models.ForeignKey(Technician,on_delete=models.CASCADE)
    Ac_no = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    bank_holder_name = models.CharField(max_length=100)
    def __str__(self):
        return self.technician_id
    
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type=='1':
            AdminHOD.objects.create(admin=instance)
        if instance.user_type=='2':
            technician = Technician.objects.create(admin=instance, present_address="")
            technician.subcategories.set([SubCategory.objects.first()])
        if instance.user_type=='3':
            
            Support.objects.create(admin=instance, address="")
            # support.can_assign_task = instance.has_perm('homofix_app.assign_task')
            # support.can_cancel_booking = instance.has_perm('homofix_app.cancel_order')
            # support.save()
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


# @receiver(post_save, sender=Addon)
# def update_booking_on_addon_save(sender, instance, **kwargs):
#     booking = instance.booking
#     for addons_product in instance.addon_products.all():
#         booking = Booking.objects.get(id=4)
#         product = Product.objects.get(id=1)
#         booking_product = BookingProduct.objects.create(booking=booking, product=product, quantity=2, total_price=200)
#         booking_product.save()
        # booking.products.add(booking_product)


# @receiver(post_save, sender=Addon)
# def update_booking_on_addon_save(sender, instance, **kwargs):
#     booking = instance.booking
#     booking.products.add(*instance.addon_products.all())
# @receiver(m2m_changed, sender=Addon.addon_products.through)
# def update_booking(sender, instance, **kwargs):
#     """
#     Update the products of the associated booking when an add-on product is added
#     or removed from an Addon instance.
#     """
#     if kwargs['action'] in ('post_add', 'post_remove', 'post_clear'):
#         booking = instance.booking
#         addon_products = instance.addon_products.all()
#         booking.products.set(list(booking.products.all()) + list(addon_products))    

# @receiver(post_save, sender=Booking)
# def update_technician_location(sender, instance, created, **kwargs):
#     if not created and instance.status == 'completed':
#         technicians = instance.task_set.values_list('technician', flat=True).distinct()
#         for technician_id in technicians:
#             latitude, longitude = get_technician_location_from_some_service(technician_id)
#             if latitude and longitude:
#                 location, created = TechnicianLocation.objects.update_or_create(
#                     technician_id=technician_id,
#                     defaults={
#                         'latitude': latitude,
#                         'longitude': longitude,
#                     }
#                 )
