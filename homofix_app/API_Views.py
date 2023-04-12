from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.authentication import BasicAuthentication
from homofix_app.serializers import LoginSerliazer,ExpertSerliazer,CustomUserSerializer,TaskSerializer,RebookingSerializer,JobEnquirySerliazer,ProductSerializer,BokingSerializer,KycSerializer,SparePartsSerializer,AddonsSerializer,TechnicianLocationSerializer,AddonsGetSerializer,TechnicianOnlineSerializer,TechnicianRechargeHistorySerializer,TechnicianWalletSerializer,TechnicianWalletHistorySerializer,TechnicianWithdrawRequestSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
# from homofix_app.EmailBackEnd import EmailBackEnd
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .models import Technician,Task,Rebooking,JobEnquiry,Product,Booking,Kyc,SpareParts,Addon,TechnicianLocation,showonline,RechargeHistory,Wallet,WalletHistory,WithdrawRequest



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

    def get_queryset(self):
        queryset = super().get_queryset()
        technician_id = self.request.query_params.get('technician_id')
       
        if technician_id:
            queryset = queryset.filter(technician_id=technician_id)
        return queryset
    
    def update(self, request, pk=None):
        try:
            rebooking = self.get_object()
            serializer = self.get_serializer(rebooking, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rebooking.DoesNotExist:
            return Response({"error": "Rebooking not found."}, status=status.HTTP_404_NOT_FOUND)

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

        
        
# ------------------------------------- show offline online -----------------------



class TechnicianOnlineViewSet(viewsets.ViewSet):
    
    def list(self, request):
        showonline_objs = showonline.objects.all()
        serializer=TechnicianOnlineSerializer(showonline_objs,many=True)
        return Response({
            'status':True,
            'message':'Show Online Offline fetched',
            'data':serializer.data
        })

    def update(self, request, pk=None):
        try:
            instance = showonline.objects.get(pk=pk)
            serializer = TechnicianOnlineSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': f'Show Online Offline with id {pk} updated',
                    'data': serializer.data
                })
            else:
                return Response({
                    'status': False,
                    'message': 'Invalid data',
                    'data': serializer.errors
                })
        except showonline.DoesNotExist:
            return Response({
                'status': False,
                'message': f'Show Online Offline with id {pk} does not exist',
            })
    
    # def create(self, request):
    #     serializer = TechnicianOnlineSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             'status': True,
    #             'message': 'New Show Online Offline created',
    #             'data': serializer.data
    #         })
    #     else:
    #         return Response({
    #             'status': False,
    #             'message': 'Invalid data',
    #             'data': serializer.errors
    #         })
    


# ----------------------------- RechargeHistory ----------------------
# @api_view(['GET'])
# def get_RechargeHistory(request):
#     todo_objs = RechargeHistory.objects.all()
#     serializer=TechnicianRechargeHistorySerializer(todo_objs,many=True)
#     return Response({
#         'status':True,
#         'message':'Recharge History fetched',
#         'data':serializer.data
#     })

@api_view(['GET'])
def get_RechargeHistory(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    queryset = RechargeHistory.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(technician_id=technician_id) # filter queryset by technician_id if it is not None
    serializer = TechnicianRechargeHistorySerializer(queryset, many=True)
    return Response({
        'status': True,
        'message': 'Recharge History fetched',
        'data': serializer.data
    })


@api_view(['POST'])
def post_rechargeHistory(request):
    try:
        data = request.data
        serializer = TechnicianRechargeHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Get the technician ID from the serializer data
            technician_id = serializer.data['technician_id']
            # Get the Wallet object for the technician
            technician_wallet = Wallet.objects.get(technician_id=technician_id)
            # Update the technician's total_share field with the amount from the serializer data
            technician_wallet.total_share += serializer.data['amount']
            technician_wallet.save()
            return Response({
                'status': True,
                'message': "success data",
                'data': serializer.data      
            })
        return Response({
            'status': False,
            'message': "invalid data",
            'data': serializer.errors  
        })
    except Exception as e:
        print(e)
        return Response({
            'status': False,
            'message': "Something went wrong",  
        })



# ------------------------ wallet --------------------------- 

@api_view(['GET'])
def get_Wallet(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    print("hellooo",technician_id)
    queryset = Wallet.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(technician_id=technician_id) 
    serializer=TechnicianWalletSerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Wallet  fetched',
        'data':serializer.data
    })


# ----------------------------------- Wallet History ----------------------------- 


@api_view(['GET'])
def get_Wallet_History(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    
    queryset = WalletHistory.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(wallet__technician_id=technician_id) 
    serializer=TechnicianWalletHistorySerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Wallet History fetched',
        'data':serializer.data
    })



# ----------------------------------- Withdraw Request ----------------------------- 


@api_view(['POST'])
def post_withdraw_req(request):
    try:
        data = request.data
        serializer = TechnicianWithdrawRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Get the technician ID from the serializer data
            # technician_id = serializer.data['technician_id']
            # # Get the Wallet object for the technician
            # technician_wallet = Wallet.objects.get(technician_id=technician_id)
            # # Update the technician's total_share field with the amount from the serializer data
            # technician_wallet.total_share += serializer.data['amount']
            # technician_wallet.save()
            return Response({
                'status': True,
                'message': "success data",
                'data': serializer.data      
            })
        return Response({
            'status': False,
            'message': "invalid data",
            'data': serializer.errors  
        })
    except Exception as e:
        print(e)
        return Response({
            'status': False,
            'message': "Something went wrong",  
        })




@api_view(['GET'])
def get_Withdraw_Req(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    
    queryset = WithdrawRequest.objects.all()
    if technician_id is not None:
        queryset = queryset.filter(technician_id=technician_id) 
    serializer=TechnicianWithdrawRequestSerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Withdraw Request Send',
        'data':serializer.data
    })