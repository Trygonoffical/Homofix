from django.contrib import admin
from . models import CustomUser,AdminHOD,Technician,Product,Category,Addons,Customer,Support,FAQ,Booking,Task

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AdminHOD)
# admin.site.register(Technician)
admin.site.register(Product)
admin.site.register(Addons)
admin.site.register(Customer)
admin.site.register(Support)
admin.site.register(FAQ)
admin.site.register(Booking)
admin.site.register(Task)




@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','admin','category']



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']
    
    
