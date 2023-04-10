from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.authentication import BasicAuthentication
from homofix_app.serializers import LoginSerliazer,ExpertSerliazer,CustomUserSerializer,TaskSerializer,RebookingSerializer,JobEnquirySerliazer,ProductSerializer,BokingSerializer,KycSerializer,SparePartsSerializer,AddonsSerializer,TechnicianLocationSerializer,AddonsGetSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
# from homofix_app.EmailBackEnd import EmailBackEnd
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.views import APIView

from .models import Technician,Task,Rebooking,JobEnquiry,Product,Booking,Kyc,SpareParts,Addon,TechnicianLocation




class LoginViewSet(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    serializer_class = LoginSerliazer
    def post(self,request,*args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        user=authenticate(request, username=username, password = password)
        
        

        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '2':
                user_data = {
                    'id': user.technician.id,
                    'username': user.username,
                    
                    # Add any other user fields you want to return
                }
                return Response({'message': 'Logged in successfully.', 'user': user_data}, status=status.HTTP_200_OK)
                # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)
           
        else:
            return Response({'message': 'Invalid login credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

      

class ExpertViewSet(ModelViewSet):
    
    authentication_classes = [BasicAuthentication]
    serializer_class = ExpertSerliazer
    queryset = Technician.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data) 
    
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    


class TaskViewSet(ModelViewSet):
    authentication_classes = [BasicAuthentication]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def list(self, request, *args, **kwargs):
        technician_id = request.query_params.get('technician_id')
        if technician_id:
            tasks = self.queryset.filter(technician=technician_id)
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)
    

    # @action(detail=False, methods=['PATCH'])
    def put(self, request):
        booking_id = request.data.get('booking_id')
        status = request.data.get('status')
        if booking_id and status:
            try:
                booking = Booking.objects.get(id=booking_id)
                booking.status = status
                booking.save()
                return Response({'success': True})
            except Booking.DoesNotExist:
                return Response({'success': False, 'message': 'Booking not found.'})
        else:
            return Response({'success': False, 'message': 'Booking id and status are required.'})



class RebookingViewSet(ModelViewSet):
    
    # authentication_classes = [BasicAuthentication]
    # serializer_class = RebookingSerializer
    # queryset = Rebooking.objects.all()

    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data) 
    queryset = Rebooking.objects.all()     
    serializer_class  = RebookingSerializer
    

# ---------------- Booking --------------------- 


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()     
    serializer_class  = BokingSerializer
     

class KycViewSet(ModelViewSet):
    queryset = Kyc.objects.all()     
    serializer_class  = KycSerializer
     

# ------------------------------- Job Enquiry --------------------------- 


class JobEnquiryViewSet(ModelViewSet):
    queryset = JobEnquiry.objects.all()     
    serializer_class  = JobEnquirySerliazer
     


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()     
    serializer_class  = ProductSerializer
     


class SparePartsViewSet(ModelViewSet):
    queryset = SpareParts.objects.all()     
    serializer_class  = SparePartsSerializer
     

class AddonsViewSet(ModelViewSet):
    queryset = Addon.objects.all()     
    serializer_class  = AddonsSerializer
     

class AddonsGetViewSet(ModelViewSet):
    queryset = Addon.objects.all()     
    serializer_class  = AddonsGetSerializer
     



# ----------------- Technician Location -------------------- 


class TechnicianLocationViewSet(ModelViewSet):
    serializer_class = TechnicianLocationSerializer
    queryset = TechnicianLocation.objects.all()
    def post(self, request):
        booking_id = request.data.get('booking_id')
        location = request.data.get('location')
        print("booking id",booking_id)
        if booking_id and location:
            try:
                booking = Booking.objects.get(id=booking_id)
                technician_location = TechnicianLocation.objects.get(
                    technician=booking.technician,
                    booking=booking
                )
                technician_location.location = location
                technician_location.save()
                return Response({'success': True})
            except (Booking.DoesNotExist, TechnicianLocation.DoesNotExist):
                return Response({'success': False, 'message': 'Booking or technician location not found.'})
        else:
            return Response({'success': False, 'message': 'Booking id and location are required.'})

        
        
