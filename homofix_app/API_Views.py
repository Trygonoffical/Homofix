from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.authentication import BasicAuthentication
from homofix_app.serializers import LoginSerliazer,CustomerLoginSerliazer,ExpertSerliazer,CustomUserSerializer,TaskSerializer,RebookingSerializer,JobEnquirySerliazer,ProductSerializer,BokingSerializer,KycSerializer,SparePartsSerializer,AddonsSerializer,TechnicianLocationSerializer,AddonsGetSerializer,TechnicianOnlineSerializer,TechnicianRechargeHistorySerializer,TechnicianWalletSerializer,TechnicianWalletHistorySerializer,TechnicianWithdrawRequestSerializer,AllTechnicianLocationSerializer,BlogSerializer,MostViewed,MostViewedSerializer,VerifyOtpSerializer,CategorySerializer,SubcategorySerializer,CustSerailizer,LoginCustomrSerializers,FeedbackSerailizer,OfferSerializer,testingBooking,HomePageSerailizer,BookingProductSerializer,CustomerLoginn,AddonsDeleteSerailizers,ApplicantCarrerSerliazer,CarrerSerliazer,BkingProductSerializer,BkingSerializer,LegalPageSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
# from homofix_app.EmailBackEnd import EmailBackEnd
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet,ModelViewSet,ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from .models import CustomUser,Technician,Task,Rebooking,JobEnquiry,Product,Booking,Kyc,SpareParts,Addon,TechnicianLocation,showonline,RechargeHistory,Wallet,WalletHistory,WithdrawRequest,HodSharePercentage,Share,AllTechnicianLocation,Blog,MostViewed,Customer,Category,SubCategory,feedback,Offer,BookingProduct,HomePageService,ApplicantCarrer,Carrer,LegalPage
from decimal import Decimal
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import random
import requests
from urllib.parse import urlencode
import urllib
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from django.utils import timezone
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import pdfkit
from .helpers import save_pdf

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
            print(booking_id)
            try:
                booking = Booking.objects.get(id=booking_id)
                task = Task.objects.get(booking=booking)
                booking.status = status
                # booking.save()
                booking.save()
                # return Response({'success': True})
                if booking.status == "Completed" and booking.online == True:
                    
                    tax_rate = 0.18
                    booking_amount = booking.total_amount
                    
                    tax_amt =booking.tax_amount
                    
                    hod_share_percentage = HodSharePercentage.objects.latest('id')
                    hod_share_percentage_value = hod_share_percentage.percentage
                   
                    hod_share = booking_amount * (hod_share_percentage_value / 100) 
                    
                    print("new hod share0",hod_share)
                    technician_share = booking_amount-hod_share
                    print("technicia sare",technician_share)
                    
                    hod_share_with_tax = hod_share + tax_amt
                    print("hod_share_with_tax",hod_share_with_tax)
                   
                    # technician_share = booking_amount - hod_share
                   
                    share = Share.objects.create(task=task,hod_share_percentage=hod_share_percentage,technician_share=technician_share,hod_share=hod_share)
                    share.save()
                    technician = task.technician
                    wallet, created = Wallet.objects.get_or_create(technician_id=technician)
                    wallet.total_share -= Decimal(str(hod_share_with_tax))
                   
                    wallet.save()
                   
                    
                if booking.status == "Completed" and booking.cash_on_service == True:
                    
                    tax_rate = 0.18
                    booking_amount = booking.total_amount
                    

                    tax_amt =booking.tax_amount
                    
                    hod_share_percentage = HodSharePercentage.objects.latest('id')
                    hod_share_percentage_value = hod_share_percentage.percentage
                    hod_share = booking_amount * (hod_share_percentage_value / 100) 
                    print("new hod share0",hod_share)
                    technician_share = booking_amount-hod_share
                    print("technicia sare",technician_share)
                    # print("testing",testing)
                    # wallet_online = hod_share+tax_amt
                    # print("Wallet online",wallet_online)
                    # print("hod share",hod_share+tax_amt)
                    hod_share_with_tax = hod_share + tax_amt
                    print("hod_share_with_tax",hod_share_with_tax)
                   
                    # technician_share = booking_amount - hod_share
                   
                    share = Share.objects.create(task=task,hod_share_percentage=hod_share_percentage,technician_share=technician_share,hod_share=hod_share_with_tax)
                    share.save()
                    technician = task.technician
                    wallet, created = Wallet.objects.get_or_create(technician_id=technician)
                    wallet.total_share += hod_share_with_tax
                   
                    wallet.save()
                   
                    
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
     

# class CustomerBookingSet(ModelViewSet):
#     queryset = Booking.objects.all()
#     serializer_class = testingBooking
    
#     def perform_create(self, serializer):
#         booking = serializer.save()
#         product_data = self.request.data.get('products', [])
        
#         for product_item in product_data:
#             product_id = product_item.get('product_id')
#             quantity = product_item.get('quantity')
            
#             product = Product.objects.get(id=product_id)
            
#             BookingProduct.objects.create(
#                 booking=booking,
#                 product=product,
#                 quantity=quantity
#             )
class BkingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BkingSerializer

class BkingProductViewSet(viewsets.ModelViewSet):
    queryset = BookingProduct.objects.all()
    serializer_class = BkingProductSerializer     

@api_view(['POST'])
def create_booking_manually(request):
    data = request.data
    # serializer = BookingCreateManuallySerailizer(data=data)
    print("ggggggggggggggg",data)
    return Response({
        'status':"ok",
        'message':data
    })

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_booking(request):
   
    data = request.data
    booking_products_data = data.pop('booking_products', [])
    
    
    serializer = BkingSerializer(data=data)
    
    if serializer.is_valid():
        # print("gggg",serializer)
        booking = serializer.save()

        # Create BookingProduct instances if available
        for booking_product_data in booking_products_data:
            booking_product_data['booking'] = booking.id
            # demo = booking_product_data.booking
            # print("ssss",demo)
            testo = booking_product_data['booking']
            print("demoooo datasaa",booking_product_data['booking']) 
            booking_product_serializer = BkingProductSerializer(data=booking_product_data)
            print("demooooo",booking_product_serializer)
            if booking_product_serializer.is_valid():
                print("gggg")
                booking_product_serializer.save()
            else:
                # If there are any errors in BookingProduct data, delete the created Booking instance
                booking.delete()
                return Response({
                    'status': 'error',
                    'message': 'Invalid BookingProduct data',
                    'errors': booking_product_serializer.errors
                })

        return Response({
            'status': 'ok',
            'data': serializer.data
        })
    else:

        return Response({
            'status': 'error',
            'message': 'Invalid Booking data',
            'errors': serializer.errors
        })

# @api_view(['POST'])
# def create_booking(request):
#     try:
#         data = request.data
#         serializer = testingBooking(data=data)
#         if serializer.is_valid():

#             print(data)
#             return Response({
#                 'status':200,
#                 'data':serializer.data
#             })
#         return Response({
#                 'status':200,
#                 'message':'some thing error',
#                 'data':serializer.errors
#             })
        
#     except Exception as e:
#         print(e)

# @api_view(['POST'])
# def create_booking(request):
#     try:
#         data = request.data
#         serializer = testingBooking(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'status': True,
#                 'message': 'Booking created successfully',
#                 'data': serializer.data
#             }, status=status.HTTP_201_CREATED)
        
#         return Response({
#             'status': False,
#             'message': 'Invalid data',
#             'data': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)
    
#     except Exception as e:
#         print(e)
#         return Response({
#             'status': False,
#             'message': 'Something went wrong'
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        
class KycViewSet(ModelViewSet):
    # queryset = Kyc.objects.all()     
    serializer_class  = KycSerializer
    def get_queryset(self):
        technician_id = self.request.query_params.get('technician_id')
        print("techincian id",technician_id)
        if technician_id is not None:
            queryset = Kyc.objects.filter(technician_id=technician_id)
        else:
            queryset = Kyc.objects.all()
        return queryset
    
    # def put(self, request):
        
        
    #     id = request.data.get('id')
    #     # booking_id = request.data.get('booking_id')
    #     technician_id = request.data.get('technician_id')
    #     bank_active = request.data.get('bank_active')
    #     # print("kyc id",id,"technician id",technician_id,'bank active',bank_active)
    #     if id and technician_id:
    #         print(id)
    #         try:
    #             kyc = Kyc.objects.get(id=id)
    #             technician_id = Technician.objects.get(id=technician_id)
    #             kyc.bank_active = bank_active
    #             # booking.save()
    #             kyc.save()
    #             return Response({'success': True,'message':'Kyc updated Successfull'})
    #         except (Booking.DoesNotExist, TechnicianLocation.DoesNotExist):
    #             return Response({'success': False, 'message': 'Something Eror.'})
    #     else:
    #         return Response({'success': False, 'message': 'Kyc id technician_id and bank_active are required.'})
    
    def put(self, request):
        id = request.data.get('id')
        technician_id = request.data.get('technician_id')
        bank_active = request.data.get('bank_active')

        if id and technician_id:
            try:
                kyc = Kyc.objects.get(id=id)
                technician = Technician.objects.get(id=technician_id)

                # Set bank_active=False for all other Kyc instances of the same Technician
                Kyc.objects.filter(technician_id=technician).exclude(id=id).update(bank_active=False)

                kyc.bank_active = bank_active
                kyc.save()

                return Response({'success': True, 'message': 'Kyc updated successfully'})
            except (Kyc.DoesNotExist, Technician.DoesNotExist):
                return Response({'success': False, 'message': 'Something went wrong'})
        else:
            return Response({'success': False, 'message': 'Kyc id, technician_id and bank_active are required.'})


# -------------------------- KYC COUNTING ------------------------------- 


# @api_view(['GET'])
# def ExpertTaskCountViewSet(request):
#     technician_id = request.GET.get('technician') # retrieve the technician_id query parameter
#     print("teccc id",technician_id)

    
#     queryset = Task.objects.filter(
#         technician=technician_id,
#         booking__status="Completed"
#     )
    
#     count = queryset.count()
#     print("couting",count)

   
    
#     return Response({
#         'status': True,
#         'message': 'Task count retrieved successfully',
#         'data': count
#     })



@api_view(['GET'])
def ExpertTaskCountViewSet(request):
    technician_id = request.GET.get('technician_id') # retrieve the technician_id query parameter
    
    queryset = Task.objects.all()
    queryset2 = Task.objects.all()
    rebooking = Rebooking.objects.all()
    # if technician_id is not None:
    booking_completed = Task.objects.filter(technician_id=technician_id,booking__status="Completed").count()
    
    new_booking_count = queryset2.filter(technician=technician_id,booking__status="Assign").count()
    print(queryset)
    rebooking_count = rebooking.filter(technician=technician_id,status="Assign").count()
    print("sss",rebooking_count)
    # serializer=TaskSerializer(queryset,many=True)
    return Response({
        'status':True,
        'message':'Wallet History fetched',
        'Booking_Completed':booking_completed,
        'rebooking_count':rebooking_count,
        'new_booking_count':new_booking_count
    })

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
    http_method_names = ['get', 'post', 'put', 'patch', 'delete'] 
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
     



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

        
# ----------------------- Technician All Location -------------------         

# class TechnicianAllLocationViewSet(ModelViewSet):
#     serializer_class = AllTechnicianLocationSerializer
#     queryset = AllTechnicianLocation.objects.all()

class TechnicianAllLocationViewSet(ModelViewSet):
    serializer_class = AllTechnicianLocationSerializer
    queryset = AllTechnicianLocation.objects.all()

    def create(self, request, *args, **kwargs):
        technician_id = request.data.get('technician_id')
        location = request.data.get('location')

        try:
            all_technician_location = AllTechnicianLocation.objects.get(technician_id=technician_id, location=location)
            serializer = AllTechnicianLocationSerializer(all_technician_location, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except AllTechnicianLocation.DoesNotExist:
            serializer = AllTechnicianLocationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        technician_id = request.data.get('technician_id')
        location = request.data.get('location')

        try:
            all_technician_location = AllTechnicianLocation.objects.get(technician_id=technician_id, location=location)
            serializer = AllTechnicianLocationSerializer(all_technician_location, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except AllTechnicianLocation.DoesNotExist:
            return self.create(request, *args, **kwargs)

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
    print("helooooooo")
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



class BlogGetViewSet(ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'title'

    def retrieve(self, request, *args, **kwargs):
        # Get the title from the URL parameters
        title = self.kwargs['title']

        # Perform the lookup based on the title field
        queryset = self.filter_queryset(self.get_queryset())
        blog = self.get_object()
        
        # You can add any additional logic or filtering here if needed
        
        serializer = self.get_serializer(blog)
        return Response(serializer.data)

class OfferGetViewSet(ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        # Get the title from the URL parameters
        name = self.kwargs['name']

        # Perform the lookup based on the title field
        queryset = self.filter_queryset(self.get_queryset())
        offer = self.get_object()
        
        # You can add any additional logic or filtering here if needed
        
        serializer = self.get_serializer(offer)
        return Response(serializer.data)






class MostViewedGetViewSet(ReadOnlyModelViewSet):
    queryset = MostViewed.objects.all()
    serializer_class = MostViewedSerializer


# ----------------------Booking Customer Details ---------------- 

class CustomerBookingViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Booking.objects.all()     
    serializer_class  = BokingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Filter customers based on the authenticated user
            queryset = Booking.objects.filter(customer__admin=user)
        else:
            # If there is no authenticated user, return an empty queryset
            queryset = Customer.objects.none()

        return queryset
     

# ----------------------- Customer Login --------------------------- 


class CustomerViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Customer.objects.all()
    serializer_class = CustSerailizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            # Filter customers based on the authenticated user
            queryset = Customer.objects.filter(admin=user)
        else:
            # If there is no authenticated user, return an empty queryset
            queryset = Customer.objects.none()

        return queryset
    def partial_update(self, request, *args, **kwargs):
        # Retrieve the customer object to update
        instance = self.get_object()

        # Check if the current user is the owner of the customer object
        if instance.admin == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
    # queryset = Customer.objects.all() 
    # print("queryset",queryset)    
    # serializer_class  = CustomerSerailizer
     

    # def get(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data) 
    

    # def put(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)

def verify_otp(otp, user):
    # Implement your OTP verification logic here
    # Compare the provided OTP with the OTP associated with the user

    # For example, assuming you have an OTP field in the CustomUser model:
    if user.otp == otp:
        return True
    else:
        return False


# class CustomerLoginViewSet(CreateAPIView):
#     authentication_classes = [BasicAuthentication]
#     serializer_class = CustomerLoginSerliazer
#     def post(self,request,*args, **kwargs):
#         otp_number = random.randint(0,9999)
#         otp_unique = str(otp_number).zfill(3)
#         phone_number = request.POST.get('phone_number')

#         request.session['phone_number'] = phone_number
#         request.session['otp'] = otp_unique
#         username = "TRYGON"
#         apikey = "E705A-DFEDC"
#         apirequest="Text"
#         sender ="TRYGON"
#         mobile=phone_number
#         message=f"Dear User {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
#         TemplateID="1707162192151162124"
#         url = f"https://sms.webtextsolution.com/sms-panel/api/http/index.php?username=TRYGON&apikey=E705A-DFEDC&apirequest=Text&sender={sender}&mobile={mobile}&message={urllib.parse.quote(message)}&route=TRANS&TemplateID=1707162192151162124&format=JSON"

#         response = requests.get(url) 
#         print("response",response)
        
#         # cust = Customer.objects.get(mobile=phone_number)
        
#         return Response({'message': 'Otp is sent your mobile number'}, status=status.HTTP_200_OK)
       


class CustomerLoginViewSet(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    serializer_class = CustomerLoginSerliazer
    
    def post(self, request, *args, **kwargs):
        otp_number = random.randint(0, 9999)
        otp_unique = str(otp_number).zfill(3)
        phone_number = request.data.get('phone_number')
       

        request.session['phone_number'] = phone_number
        request.session['otp'] = otp_unique
        ottt = request.session.get('otp', 'Default value if key does not exist')
        
        
        username = "TRYGON"
        apikey = "E705A-DFEDC"
        apirequest = "Text"
        sender = "TRYGON"
        mobile = phone_number
        message = f"Dear User {otp_unique} is the OTP for your login at Trygon. In case you have not requested this, please contact us at info@trygon.in"
        template_id = "1707162192151162124"
        
        url = f"https://sms.webtextsolution.com/sms-panel/api/http/index.php?username=TRYGON&apikey=E705A-DFEDC&apirequest=Text&sender={sender}&mobile={mobile}&message={urllib.parse.quote(message)}&route=TRANS&TemplateID=1707162192151162124&format=JSON"
        
        response = requests.get(url) 
        
        
        return Response({'message': 'OTP is sent to your mobile number','otp_session':ottt}, status=status.HTTP_200_OK)
class CustomerLoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            
            serializer = LoginCustomrSerializers(data = data)
            if serializer.is_valid():
                password = serializer.data['phone_number']
                
                if Customer.objects.filter(mobile=password).exists():
                    cus = Customer.objects.get(mobile=password)
                    username = cus.admin.username
                    

                    user = authenticate(password=password,username=username)
                    if user is None:
                        return Response({
                        'status':400,
                        'message':'Invalid Password',
                        'data':{}
                        })

                    user_type = user.user_type
                    if user_type == '4':
                        user_data = {
                            'id': user.customer.id,
                            'mobile': user.customer.mobile,
                            'message':'Login Success'
                            # 'username': user.username,
                            
                            # Add any other user fields you want to return
                    }
                    refresh = RefreshToken.for_user(user)

                    return Response({
                        # 'refresh': str(refresh),
                        'token': str(refresh.access_token),
                        'Customer': user_data
                    })
                else:
                    last_three_digits = password[-3:]
                    userr = "user"
                    
                    user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
                    user.set_password(password)
                    user.customer.mobile = password
                    user.save()
                    

                    custm = Customer.objects.get(mobile=password)
                    usernme = custm.admin.username
                   
                    usrr=authenticate(request,username=usernme, password = password)
                    if usrr is None:
                        return Response({
                        'status':400,
                        'message':'Invalid Password',
                        'data':{}
                        })
                    user_type = user.user_type
                    if user_type == '4':
                        user_data = {
                            'id': user.customer.id,
                            'username': user.username,
                            
                            # Add any other user fields you want to return
                    }
                    refresh = RefreshToken.for_user(usrr)

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': user_data
                    })
            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)




# -------------------------------- feedback --------------------------

class FeedbackViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = feedback.objects.all()
    serializer_class = FeedbackSerailizer
    permission_classes = [IsAuthenticated]

# class CustomerVerifyOtp(CreateAPIView):
#     authentication_classes = [BasicAuthentication]
#     serializer_class = VerifyOtpSerializer
#     def post(self,request,*args, **kwargs):
        
#         mobile = request.session.get('phone_number', 'Default value if key does not exist')
        
#         if Customer.objects.filter(mobile="llll").exists():
            
#             cust = Customer.objects.get(mobile=mobile)
#             username = cust.admin.username
#             print("userneeeeeeeeameeee",username)
            
#             user=authenticate(request,username=username, password = mobile)
#             # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)

#             if user!=None:
#                 login(request,user)
#                 user_type = user.user_type
#                 if user_type == '4':
#                     user_data = {
#                         'id': user.customer.id,
#                         'username': user.username,
                        
#                         # Add any other user fields you want to return
#                     }

#                     refresh = RefreshToken.for_user(user)
#                     return Response({
#                     # 'refresh': str(refresh),
#                     'token': str(refresh.access_token),
#                 })
            
#                     # return Response({'message': 'Logged in successfully.','user': user_data}, status=status.HTTP_200_OK)
#         else:
#                 last_three_digits = mobile[-3:]
#                 userr = "user"
#                 user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
#                 user.set_password(mobile)
#                 user.customer.mobile = mobile
#                 user.save()
                

#                 custm = Customer.objects.get(mobile=mobile)
#                 usernme = custm.admin.username
               
#                 usrr=authenticate(request,username=usernme, password = mobile)
#                 if usrr!=None:
#                     login(request,user)
#                     user_type = usrr.user_type
#                     if user_type == '4':
#                         user_data1 = {
#                             'id': usrr.customer.id,
#                             'username': usrr.username,
                            
#                             # Add any other user fields you want to return
#                         }
#                         refresh = RefreshToken.for_user(usrr)
#                         return Response({
#                         'refresh': str(refresh),
#                         'access': str(refresh.access_token),
#                          })
                
#                         # return Response({'message': 'Logged in successfully.','user': user_data1}, status=status.HTTP_200_OK)
#         return Response({'message': 'Invalid Otp.'}, status=status.HTTP_401_UNAUTHORIZED)

        
                
class CustomerVerifyOtp(CreateAPIView):
    authentication_classes = [BasicAuthentication]
    serializer_class = VerifyOtpSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        Otp = data.get('OTPP')
        print("hellooooo")
        
        otp_nUMB = request.session.get('otp', 'Default value if key does not exist')
        print("OTP from session:", otp_nUMB)
        mobile = request.session.get('phone_number', 'Default value if key does not exist')
        
        return Response({
            'otp_input': Otp,
            'otp_session': otp_nUMB,
        })       # if otp == otp_no:
        #     if Customer.objects.filter(mobile=mobile).exists():
                
        #             cust = Customer.objects.get(mobile=mobile)
        #             username = cust.admin.username
        #             print("usernameeee",username)
                    
        #             user=authenticate(request,username=username, password = mobile)
                    # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)

        #             if user!=None:
        #                 login(request,user)
        #                 user_type = user.user_type
        #                 if user_type == '4':
        #                     user_data = {
        #                         'id': user.customer.id,
        #                         'username': user.username,
                                
        #                         # Add any other user fields you want to return
        #                     }
        #                     refresh = RefreshToken.for_user(user)
        #                     return Response({
        #                     # 'refresh': str(refresh),
        #                     'token': str(refresh.access_token),
        #                     'message': 'Logged in successfully.','user': user_data
        #                 })
                    
        #                     # return Response({'message': 'Logged in successfully.','user': user_data}, status=status.HTTP_200_OK)
        #     else:
        #         last_three_digits = mobile[-3:]
        #         userr = "user"
        #         user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
        #         user.set_password(mobile)
        #         user.customer.mobile = mobile
        #         user.save()
                

        #         custm = Customer.objects.get(mobile=mobile)
        #         usernme = custm.admin.username
        #         print("usernammeee",usernme)
        #         usrr=authenticate(request,username=usernme, password = mobile)
        #         if usrr!=None:
        #                 login(request,user)
        #                 user_type = usrr.user_type
        #                 if user_type == '4':
        #                     user_data1 = {
        #                         'id': usrr.customer.id,
        #                         'username': usrr.username,
                                
        #                         # Add any other user fields you want to return
        #                     }
        #                     refresh = RefreshToken.for_user(usrr)
        #                     return Response({
        #                     # 'refresh': str(refresh),
        #                     'token': str(refresh.access_token),
        #                     'message': 'Logged in successfully.','user': user_data1
        #                 })
                    
        #                     # return Response({'message': 'Logged in successfully.','user': user_data1}, status=status.HTTP_200_OK)
        # return Response({'message': 'Invalid Otp.'}, status=status.HTTP_401_UNAUTHORIZED)

        
# class CustomerVerifyOtp(CreateAPIView):
#     authentication_classes = [BasicAuthentication]
#     serializer_class = VerifyOtpSerializer
#     def post(self,request,*args, **kwargs):
#         otp = request.POST.get('otp')
#         otp_no = request.session.get('otp', 'Default value if key does not exist')
#         mobile = request.session.get('phone_number', 'Default value if key does not exist')
#         if otp == otp_no:
#             if Customer.objects.filter(mobile=mobile).exists():
                
#                     cust = Customer.objects.get(mobile=mobile)
#                     username = cust.admin.username
#                     print("usernameeee",username)
                    
#                     user=authenticate(request,username=username, password = mobile)
#                     # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)

#                     if user!=None:
#                         login(request,user)
#                         user_type = user.user_type
#                         if user_type == '4':
#                             user_data = {
#                                 'id': user.customer.id,
#                                 'username': user.username,
                                
#                                 # Add any other user fields you want to return
#                             }
#                             refresh = RefreshToken.for_user(user)
#                             return Response({
#                             # 'refresh': str(refresh),
#                             'token': str(refresh.access_token),
#                             'message': 'Logged in successfully.','user': user_data
#                         })
                    
#                             # return Response({'message': 'Logged in successfully.','user': user_data}, status=status.HTTP_200_OK)
#             else:
#                 last_three_digits = mobile[-3:]
#                 userr = "user"
#                 user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
#                 user.set_password(mobile)
#                 user.customer.mobile = mobile
#                 user.save()
                

#                 custm = Customer.objects.get(mobile=mobile)
#                 usernme = custm.admin.username
#                 print("usernammeee",usernme)
#                 usrr=authenticate(request,username=usernme, password = mobile)
#                 if usrr!=None:
#                         login(request,user)
#                         user_type = usrr.user_type
#                         if user_type == '4':
#                             user_data1 = {
#                                 'id': usrr.customer.id,
#                                 'username': usrr.username,
                                
#                                 # Add any other user fields you want to return
#                             }
#                             refresh = RefreshToken.for_user(usrr)
#                             return Response({
#                             # 'refresh': str(refresh),
#                             'token': str(refresh.access_token),
#                             'message': 'Logged in successfully.','user': user_data1
#                         })
                    
#                             # return Response({'message': 'Logged in successfully.','user': user_data1}, status=status.HTTP_200_OK)
#         return Response({'message': 'Invalid Otp.'}, status=status.HTTP_401_UNAUTHORIZED)

        
                
                

            
# ------------------------ Category ------------------------ 



class CategoryGetViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
            

# ------------------------ Subcategory ------------------------ 


# class SubcategoryGetViewSet(ReadOnlyModelViewSet):
#     queryset = SubCategory.objects.all()
#     serializer_class = SubcategorySerializer

class SubcategoryGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('Category_id')
        if category_id is not None:
            queryset = queryset.filter(Category_id=category_id)
        return queryset

class LoginAPI(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = LoginCustomrSerializers(data = data)
            if serializer.is_valid():
                password = serializer.data['password']
                cus = Customer.objects.get(mobile=password)
                username = cus.admin.username
                print("usernameee",username)

                user = authenticate(password=password,username=username)
                if user is None:
                    return Response({
                    'status':400,
                    'message':'Invalid Password',
                    'data':{}
                    })
                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)


class BlogByTitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'title'            





class HomePageServiceViewSet(ModelViewSet):
    queryset = HomePageService.objects.all()     
    serializer_class  = HomePageSerailizer







class CustomerLogin(APIView):
    def post(self,request):
        data = request.data 
        serializer = CustomerLoginn(data = data)
        if serializer.is_valid():
            # return Response(data)
            phone_number = serializer.validated_data.get('phone_number')
            # print("helooo phone",phone_number)
            # return Response({
            #     'phone_number':phone_number
            # })
            
            if Customer.objects.filter(mobile=phone_number).exists():
            
                cust = Customer.objects.get(mobile=phone_number)
                username = cust.admin.username
                print("usernameeee",username)
                
                user=authenticate(request,username=username, password = phone_number)
                # return Response({'message': 'Logged in successfully.'}, status=status.HTTP_200_OK)

                if user!=None:
                    login(request,user)
                    user_type = user.user_type
                    if user_type == '4':
                        user_data = {
                            'id': user.customer.id,
                            'username': user.username,
                            
                            # Add any other user fields you want to return
                        }
                        refresh = RefreshToken.for_user(user)
                        return Response({
                        # 'refresh': str(refresh),
                        'token': str(refresh.access_token),
                        'message': 'Logged in successfully.','user': user_data
                    })
                
                        # return Response({'message': 'Logged in successfully.','user': user_data}, status=status.HTTP_200_OK)
            else:
                last_three_digits = phone_number[-3:]
                userr = "user"
                user = CustomUser.objects.create(username=userr+last_three_digits, user_type='4')    
                user.set_password(phone_number)
                user.customer.mobile = phone_number
                user.save()

                
                    
                custm = Customer.objects.get(mobile=phone_number)
                usernme = custm.admin.username
                print("usernammeee",usernme)
                usrr=authenticate(request,username=usernme, password = phone_number)
                if usrr!=None:
                    login(request,user)
                    user_type = usrr.user_type
                    if user_type == '4':
                        user_data1 = {
                            'id': usrr.customer.id,
                            'username': usrr.username,
                            
                            # Add any other user fields you want to return
                        }
                        refresh = RefreshToken.for_user(usrr)
                        return Response({
                        # 'refresh': str(refresh),
                        'token': str(refresh.access_token),
                        'message': 'Logged in successfully.','user': user_data1
                    })
        
        # try:
            
            
        #     if serializer.is_valid():
        #         password = serializer.data['password']
        #         cus = Customer.objects.get(mobile=password)
        #         username = cus.admin.username
        #         print("usernameee",username)

        #         user = authenticate(password=password,username=username)
        #         if user is None:
        #             return Response({
        #             'status':400,
        #             'message':'Invalid Password',
        #             'data':{}
        #             })
        #         refresh = RefreshToken.for_user(user)

        #         return Response({
        #             'refresh': str(refresh),
        #             'access': str(refresh.access_token),
        #         })

        #     return Response({
        #         'status':400,
        #         'message':'something went wrong',
        #         'data':serializer.errors
        #     })
        # except Exception as e:
        #     print(e)

class addonsDelete(APIView):
    def delete(self, request):
        data = request.data
        serializer = AddonsDeleteSerailizers(data=data)
        if serializer.is_valid():
            try:
                id = serializer.data['id']
                addon = Addon.objects.get(id=id)
                addon.delete()
                return Response({
                    'message': "Addons Delete Successfully"
                })
            except Addon.DoesNotExist:
                return Response({
                    'message': "Addon not found"
                })
        return Response({
            'message': "Invalid Id"
        })     


class ApplicantCarrerViewSet(ModelViewSet):
    queryset = ApplicantCarrer.objects.all()     
    serializer_class  = ApplicantCarrerSerliazer



class CarrerViewedGetViewSet(ReadOnlyModelViewSet):
    queryset = Carrer.objects.filter(status = True)
    serializer_class = CarrerSerliazer    



# ------------------------- Lega Page ----------------------- 
class LegalPageViewSet(ReadOnlyModelViewSet):
    queryset = LegalPage.objects.all()
    serializer_class = LegalPageSerializer    



# ------------------- generate PDF ------------------     
@api_view(['GET'])
def generate_invoice_pdf(request):
    category_objs = Category.objects.all()
    params = {
        # 'today':datetime
        'category_objs':category_objs
    }
    file_name,status= save_pdf(params)
    if not status:
        return Response({
       'status':400
    })

    # file_path = f'/static/invoice/{file_name}'
    # print("file path",file_path)

    
    return Response({
       'status':200,
       'path':f'/media/{file_name}'
    })