from rest_framework import serializers
from .models import Technician,CustomUser

class LoginSerliazer(serializers.Serializer):
    username = serializers.CharField
    password = serializers.CharField
    class Meta:
       
        fields = ('username','password')  

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
             