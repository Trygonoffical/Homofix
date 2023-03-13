from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.authentication import BasicAuthentication
from homofix_app.serializers import LoginSerliazer,ExpertSerliazer,CustomUserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
# from homofix_app.EmailBackEnd import EmailBackEnd
from rest_framework.viewsets import ViewSet,ModelViewSet


from .models import Technician



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
                    'id': user.id,
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

    
