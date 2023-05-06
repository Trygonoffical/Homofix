from django.contrib import admin
from . models import CustomUser,AdminHOD,Technician,Product,Category,SpareParts,Customer,Support,FAQ,Booking,Task,Rebooking,BookingProduct,SubCategory,ContactUs,JobEnquiry,HodSharePercentage,Payment,Addon,Wallet,TechnicianLocation,Kyc,showonline,RechargeHistory,Share,AllTechnicianLocation,WithdrawRequest,Attendance,Blog

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
# admin.site.register(Wallet)
admin.site.register(TechnicianLocation)
admin.site.register(Kyc)
admin.site.register(showonline)
admin.site.register(RechargeHistory)
admin.site.register(Share)
admin.site.register(AllTechnicianLocation)
admin.site.register(WithdrawRequest)
admin.site.register(Attendance)
admin.site.register(Blog)




@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','admin']

@admin.register(Wallet)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','total_share']

@admin.register(SpareParts)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','product','spare_part','price','description']


@admin.register(Booking)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','subtotal','total_amount','tax_amount','total_addons']


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display=['id','admin','can_new_booking','can_cancel_booking','can_rebooking','can_assign_task','can_expert_create','can_contact_us_enquiry']

    

@admin.register(Addon)
class SupportAdmin(admin.ModelAdmin):
    list_display=['id','booking_prod_id','spare_parts_id','quantity','description','date']

    



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']
    

@admin.register(JobEnquiry)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','mobile','email','resume','date']
    
    
