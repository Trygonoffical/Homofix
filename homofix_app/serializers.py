from rest_framework import serializers
from .models import Technician,CustomUser,Task,Booking,Product,Customer,Rebooking,BookingProduct,JobEnquiry
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

class LoginSerliazer(serializers.Serializer):
    username = serializers.CharField
    password = serializers.CharField
    class Meta:
       
        fields = ('id','username','password')  
        # fields = ['username', 'email', 'first_name', 'last_name']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

 
class ExpertSerliazer(serializers.ModelSerializer):
    admin = CustomUserSerializer()
    class Meta:
        model = Technician
        fields = "__all__"
        # fields = ['reference_id','created_at','updated_at','admin_id']   
        # depth = 1    




# ------------------ Task ------------------------ 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']

class CustomerSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    class Meta:
        model = Customer
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    
    warranty_desc = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = "__all__"

    def get_warranty_desc(self, obj):

        return obj.warranty_desc.replace('\r\n', '').strip().replace('<p>', '').replace('</p>', '')



class BookingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    products = ProductSerializer(many=True)
    

    class Meta:
        model = Booking
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    booking = BookingSerializer()
 

    class Meta:
        model = Task
        fields = "__all__"



# ----------------------- Rebooking ------------------------

# class customerSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='admin.username', read_only=True)

#     class Meta:
#         model = Customer
#         fields = ['id', 'username', 'address', 'mobile', 'state']

# class BokingSerializer(serializers.ModelSerializer):
#     customer = customerSerializer()

#     class Meta:
#         model = Booking
#         fields = ['id', 'customer',  'status']        
        
# class BookingProductSerializer(serializers.ModelSerializer):
#     booking = BokingSerializer()
#     product = serializers.StringRelatedField()
    

#     class Meta:
#         model = BookingProduct
#         fields = ['id', 'product', 'quantity', 'total_price']


# class RebookingSerializer(serializers.ModelSerializer):
#     booking_product = BookingProductSerializer()



# class customerSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='admin.username', read_only=True)

#     class Meta:
#         model = Customer
#         fields = ['id', 'username', 'address', 'mobile', 'state']

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price']


# class BookingProductSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()

#     class Meta:
#         model = BookingProduct
#         fields = ['id', 'product', 'total_price']


# class BokingSerializer(serializers.ModelSerializer):
#     customer = customerSerializer()
#     products = BookingProductSerializer(source='bookingproduct_set', many=True)

#     class Meta:
#         model = Booking
#         fields = ['id', 'customer', 'booking_date', 'is_verified', 'supported_by', 'status', 'products']


# class RebookingSerializer(serializers.ModelSerializer):
#     booking_product = BookingProductSerializer()
#     # technician = serializers.StringRelatedField()
#     booking_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
#     # booking = BokingSerializer()

#     class Meta:
#         model = Rebooking
#         fields = "__all__"

   
     

#     class Meta:
#         model = Rebooking
#         fields = "__all__"


class customerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='admin.username', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'username', 'address', 'mobile', 'state']


class ProductSerializerr(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'product_pic']


class BokingSerializer(serializers.ModelSerializer):
    customer = customerSerializer()
    # products = BookingProductSerializer(source='bookingproduct_set', many=True)

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'booking_date', 'is_verified', 'supported_by', 'status', 'products']


class BookingProductSerializer(serializers.ModelSerializer):
    product = ProductSerializerr()
    booking = BokingSerializer()
    
    # booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    class Meta:
        model = BookingProduct
        fields = ['id', 'booking', 'product', 'quantity', 'total_price']

class TechnicianSerializer(serializers.ModelSerializer):
    admin_id = serializers.ReadOnlyField(source='admin.id')

    class Meta:
        model = Technician
        fields = ['admin_id']



class RebookingSerializer(serializers.ModelSerializer):
    booking_product = BookingProductSerializer()
    
   
    class Meta:
        model = Rebooking
        fields = "__all__"






# --------------------------- JOb ENQUIRY ------------------------------- 

class JobEnquirySerliazer(serializers.ModelSerializer):
    class Meta:
        model = JobEnquiry
        fields = "__all__"