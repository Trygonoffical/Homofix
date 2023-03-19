from rest_framework import serializers
from .models import Technician,CustomUser,Task,Booking,Product
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
        fields = ['username','email']

 
class ExpertSerliazer(serializers.ModelSerializer):
    admin = CustomUserSerializer()
    class Meta:
        model = Technician
        fields = "__all__"
        # fields = ['reference_id','created_at','updated_at','admin_id']   
        # depth = 1    




class ProductSerializer(serializers.ModelSerializer):
    
    warranty_desc = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = "__all__"

    def get_warranty_desc(self, obj):

        return obj.warranty_desc.replace('\r\n', '').strip().replace('<p>', '').replace('</p>', '')


# ------------------ Task ------------------------ 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']




class BookingSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Booking
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    booking = BookingSerializer()
    
    

    class Meta:
        model = Task
        fields = "__all__"

    
