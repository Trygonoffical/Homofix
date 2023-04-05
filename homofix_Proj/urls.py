
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from homofix_app import API_Views
router = DefaultRouter()
router.register('Expert', API_Views.ExpertViewSet,basename="Expert")
router.register('Task', API_Views.TaskViewSet,basename="Task")
router.register('Rebooking', API_Views.RebookingViewSet,basename="Rebooking")
router.register('JobEnquiry', API_Views.JobEnquiryViewSet,basename="JobEnquiry")
router.register('Product', API_Views.ProductViewSet,basename="Product")
router.register('Booking', API_Views.BookingViewSet,basename="Booking")
router.register('Kyc', API_Views.KycViewSet,basename="Kyc")
router.register('SpareParts', API_Views.SparePartsViewSet,basename="SpareParts")
router.register('Addons', API_Views.AddonsViewSet,basename="Addons")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('homofix_app.urls')),
    path("Support/",include('homofix_app.support_urls')),
    path("Technician/",include('homofix_app.technician_urls')),
    path('api/Login/',API_Views.LoginViewSet.as_view(),name="api_login"),
    path('api/',include(router.urls),name="api"),
   
]
