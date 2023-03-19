
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from homofix_app import API_Views
router = DefaultRouter()
router.register('Expert', API_Views.ExpertViewSet,basename="Expert")
router.register('Task', API_Views.TaskViewSet,basename="Task")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('homofix_app.urls')),
    path("Support/",include('homofix_app.support_urls')),
    path("Technician/",include('homofix_app.technician_urls')),
    path('api/Login/',API_Views.LoginViewSet.as_view(),name="api_login"),
    path('api/',include(router.urls),name="api"),
   
]
