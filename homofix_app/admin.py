from django.contrib import admin
from . models import CustomUser,AdminHOD,Technician,Product,Category,SpareParts,Customer,Support,FAQ,Booking,Task,Rebooking,BookingProduct,SubCategory,ContactUs,JobEnquiry,HodSharePercentage,Payment,Addon,Wallet,TechnicianLocation

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AdminHOD)
# admin.site.register(Technician)
admin.site.register(Product)
# admin.site.register(SpareParts)
admin.site.register(Customer)
# admin.site.register(Support)
admin.site.register(FAQ)
# admin.site.register(Booking)
admin.site.register(Task)
admin.site.register(Rebooking)
admin.site.register(BookingProduct)
admin.site.register(SubCategory)
admin.site.register(ContactUs)
admin.site.register(HodSharePercentage)
admin.site.register(Payment)
# admin.site.register(Addon)
admin.site.register(Wallet)
admin.site.register(TechnicianLocation)




@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','admin']

@admin.register(SpareParts)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','product','spare_part','price','description']


@admin.register(Booking)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','total_amount']


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display=['id','admin','can_new_booking','can_cancel_booking','can_rebooking','can_assign_task','can_expert_create','can_contact_us_enquiry']

    

@admin.register(Addon)
class SupportAdmin(admin.ModelAdmin):
    list_display=['id','booking_prod_id','addon_products','quantity','description','date']

    



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']
    

@admin.register(JobEnquiry)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','mobile','email','resume','date']
    
    
