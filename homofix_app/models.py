from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import generate_ref_code

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Technician"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


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
    updated_at=models.DateField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.category_name
    

   
    


class Technician(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    mobile = models.IntegerField(blank=True,null=True)
    user_id = models.CharField(max_length=12,blank=True)
    Father_name = models.CharField(max_length=100,null=True,blank=True)
    present_address = models.TextField(null=True,blank=True)
    permanent_address = models.TextField(null=True,blank=True)
    Id_Proof = models.CharField(max_length=100,null=True,blank=True)
    id_type = models.CharField(max_length=100,null=True,blank=True)
    id_number = models.CharField(max_length=50,null=True,blank=True)
    expert_in = models.CharField(max_length=50,null=True,blank=True)
    serving_area = models.CharField(max_length=100,null=True,blank=True)
    highest_qualification = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    objects=models.Manager()


    def save(self, *args, **kwargs):
        if self.user_id == "":
            user_id = (generate_ref_code())
            self.user_id = user_id
        super().save(*args, **kwargs)


class Product(models.Model):
    product_pic = models.ImageField(upload_to = 'media/product_pic')
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=50)
    created_at=models.DateField(auto_now_add=True)


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            category = Category.objects.first()
            Technician.objects.create(admin=instance,category=category,present_address="")




@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.technician.save()
   
    
