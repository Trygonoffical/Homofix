from django.contrib import admin
from . models import CustomUser,AdminHOD,Technician,Product,Category

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AdminHOD)
# admin.site.register(Technician)
admin.site.register(Product)

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display=['id','admin','category']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']
