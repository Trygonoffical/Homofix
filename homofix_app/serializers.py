from rest_framework import serializers
from .models import Technician,CustomUser,Task,Booking,Product,Customer,Rebooking,BookingProduct,JobEnquiry,Kyc,SpareParts,Addon,TechnicianLocation,showonline,RechargeHistory,Wallet,WalletHistory,WithdrawRequest,AllTechnicianLocation,Blog,MostViewed,Category,SubCategory,feedback,Offer,HomePageService

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
        fields = ['username','email','first_name']

 
class ExpertSerliazer(serializers.ModelSerializer):
    admin = CustomUserSerializer()
    class Meta:
        model = Technician
        fields = "__all__"
        # fields = ['reference_id','created_at','updated_at','admin_id']   
        # depth = 1    



# ------------------ Task ------------------------ 


class BookingprdSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    
    class Meta:
        model = BookingProduct
        fields = ('id', 'product_id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username',"first_name"]

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

class techSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = "__all__"



class BookingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingProduct
        fields = ['id','product']



class BookingSerializer(serializers.ModelSerializer):
    bookingproduct_set = BookingProductSerializer(many=True)
    customer = CustomerSerializer()
    products = ProductSerializer(many=True)
    # total_amount = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    
    

    class Meta:
        model = Booking
        fields = "__all__"




class TaskSerializer(serializers.ModelSerializer):
    booking = BookingSerializer()
    technician = techSerializer()
    # booking_product = BookingprdSerializer(source='booking.bookingproduct_set', many=True)
  

    class Meta:
        model = Task
        fields = "__all__"



# class BokingSerializer(serializers.ModelSerializer):
#     # booking = BookingSerializer()
 

#     class Meta:
#         model = Booking
#         fields = "__all__"


class KycSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kyc
        fields = "__all__"


# ------------------------------- PRODUCT ------------------

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
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


class testingBooking(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = "__all__"
    
    def get_products(self, booking):
        booking_products = BookingProduct.objects.filter(booking=booking)
        product_data = []
        
        for booking_product in booking_products:
            product_data.append({
                'product_id': booking_product.product.id,
                'quantity': booking_product.quantity,
                # Include any other product details you want to display
            })
        
        return product_data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = self.get_products(instance)
        return representation




class BokingSerializer(serializers.ModelSerializer):
    # customer = customerSerializer()
    # products = BookingProductSerializer(source='bookingproduct_set', many=True)

    class Meta:
        model = Booking
        fields = "__all__"
        # fields = ['id', 'customer', 'booking_date', 'is_verified', 'supported_by', 'status', 'products']


class BookingProductSerializer(serializers.ModelSerializer):
    product = ProductSerializerr()
    booking = BookingSerializer()
    
    # booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())

    class Meta:
        model = BookingProduct
        fields = ['id', 'booking', 'product', 'quantity', 'total_price']

class TechnicianSerializer(serializers.ModelSerializer):
    admin_id = serializers.ReadOnlyField(source='admin.id')

    class Meta:
        model = Technician
        # fields = ['admin_id']
        fields = "__all__"



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



# --------------------------------------- SparePARTS ----------------------         


class SparePartsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SpareParts
        fields = ['id','product','spare_part','price','description']

# --------------------------------------- SparePARTS ----------------------         

# class AddonsSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Addon
#         fields = "__all__"


class BookingProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingProduct
        fields = ['id','booking', 'product', 'quantity', 'total_price', 'total_price_with_tax']


# class AddonsSerializer(serializers.ModelSerializer):
#     # booking_prod_id = BookingProdSerializer()
    
#     class Meta:
#         model = Addon
#         # fields = ['id', 'booking_product', 'addon_products', 'quantity', 'date', 'description']
#         fields = "__all__"




class SparPartsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SpareParts
        fields = ['id','product','spare_part','price','description']


class BookingProductAddonSerializer(serializers.ModelSerializer):
    # booking = serializers.IntegerField(source='booking.id')
    booking= BookingSerializer()
    # technician_id = serializers.IntegerField(source='booking.technician.id')
    
    class Meta:
        model = BookingProduct
        fields = ['id','booking', 'product', 'quantity', 'total_price', 'total_price_with_tax']



class AddonsSerializer(serializers.ModelSerializer):
    # booking_prod_id = BookingProductAddonSerializer()
    # addon_products = SparPartsSerializer()

    class Meta:
        model = Addon
        fields = ['id', 'booking_prod_id', 'spare_parts_id', 'quantity', 'date', 'description']


class AddonsGetSerializer(serializers.ModelSerializer):
    # booking_prod_id = BookingProductAddonSerializer()
    spare_parts_id = SparePartsSerializer()
    booking_id = serializers.ReadOnlyField(source='booking_prod_id.booking.id')

    class Meta:
        model = Addon
        fields = ['id','booking_id', 'booking_prod_id', 'spare_parts_id', 'quantity', 'date', 'description']


# ---------------------------------------- Technician Location ------------- 

class TechnicianLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=TechnicianLocation
        fields = ['technician_id','booking_id','location']

# ------------------------------ All Technician Location ---------------------- 

class AllTechnicianLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model=AllTechnicianLocation
        fields = "__all__"


# --------------------------- Online Offline -------------------------- 
class TechnicianOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = showonline
        # fields = '__all__'
        exclude = ['date']




# ----------------------------------- RechargeHistory ------------------
class TechnicianRechargeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeHistory
        fields = '__all__'
        # exclude = ['date']


# ------------------------- wallet -------------------- 

class TechnicianWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
        # exclude = ['date']

# --------------------- Wallet History --------------------- 
class TechnicianWalletHistorySerializer(serializers.ModelSerializer):
    # technician_id = serializers.IntegerField(source='wallet.technician_id')
    technician_id = serializers.PrimaryKeyRelatedField(source='wallet.technician_id', read_only=True)
    class Meta:
        model = WalletHistory
        # fields = '__all__'
        fields = ('id', 'technician_id', 'type', 'amount', 'description', 'date')



# ------------------------- WithdrawRequest ------------------------- 

class TechnicianWithdrawRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        
        fields = '__all__'
    
    

class OfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        
        fields = '__all__'
    
    

   


class MostViewedSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_id.name', read_only=True)
    class Meta:
        model = MostViewed
        fields = ['product_id', 'product_name', 'img']


# ----------------------------- Category ------------------- 


class CategorySerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Category
        fields = ['id','icon','category_name']



# ----------------------------- Sub-Category ------------------- 



class SubcategorySerializer(serializers.ModelSerializer):
    Category_name = serializers.CharField(source='Category_id.category_name', read_only=True)    

    class Meta:
        model = SubCategory
        fields = ['id','subcategory_image','name','Category_id','Category_name']


# ------------------------- Reebooking -------------------------         

# class TechnicianRebookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Rebooking
#         fields = '__all__'




# ---------------------------- Customer Login ------------------------------


class CustomerLoginSerliazer(serializers.Serializer):
    
    phone_number = serializers.CharField
   
    class Meta:
       
        fields = ('phone_number')  
        

class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField
    class Meta:
        fields = ('otp')  




class CustSerailizer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='admin.username')
    class Meta:
        model=Customer
        fields = '__all__'
        ['id', 'admin', 'username', 'address', 'mobile', 'city', 'state', 'area', 'zipcode']
        
# -------------------- feedback ------------------------- 


class FeedbackSerailizer(serializers.ModelSerializer):
    # username = serializers.ReadOnlyField(source='admin.username')
    class Meta:
        model=feedback
        fields = '__all__'
        # ['id', 'admin', 'username', 'address', 'mobile', 'city', 'state', 'area', 'zipcode']
        


class LoginCustomrSerializers(serializers.Serializer):
    phone_number = serializers.CharField()



# --------------------------------- Home Page Service API ------------ 

class SubcategrySerializer(serializers.ModelSerializer):
    # Category_name = serializers.CharField(source='Category_id.category_name', read_only=True)    

    class Meta:
        model = SubCategory
        fields = ['id','subcategory_image','name']




class HomePageSerailizer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = SubcategrySerializer(many=True, read_only=True, source='category_id.subcategory_set')
    
    
    class Meta:
        model=HomePageService
        
        fields = ['id', 'title', 'category_id', 'subcategory']
        