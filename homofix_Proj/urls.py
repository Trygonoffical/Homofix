
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from homofix_app import API_Views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
router.register('Addons-GET', API_Views.AddonsGetViewSet,basename="Addons-GET")
router.register('Location', API_Views.TechnicianLocationViewSet,basename="Location")
router.register('OnlineOffline', API_Views.TechnicianOnlineViewSet, basename='OnlineOffline')
router.register('ExpertAllLocation', API_Views.TechnicianAllLocationViewSet, basename='ExpertAllLocation')
router.register('Blog', API_Views.BlogGetViewSet, basename='Blog')
router.register('MostViewed-Get', API_Views.MostViewedGetViewSet, basename='MostViewed')
router.register('Category-Get', API_Views.CategoryGetViewSet, basename='CategoryGetViewSet')
router.register('Subcategory-Get', API_Views.SubcategoryGetViewSet, basename='SubcategoryGetViewSet')
router.register('Customer', API_Views.CustomerViewSet, basename='Customer')
router.register('Customer/Booking/Details', API_Views.CustomerBookingViewSet, basename='CustomerBookingViewSet')
router.register('Feedback', API_Views.FeedbackViewSet, basename='feedback')
router.register('Offer', API_Views.OfferGetViewSet, basename='offer')
router.register('HomePageService', API_Views.HomePageServiceViewSet, basename='HomePageService')
router.register('Carrer-Get', API_Views.CarrerViewedGetViewSet, basename='carrer-get')
router.register('ApplicantCarrer', API_Views.ApplicantCarrerViewSet, basename='carrer')
router.register('Bking', API_Views.BkingViewSet, basename='booking')
router.register('booking-products', API_Views.BkingProductViewSet, basename='booking-products')
router.register('Legal-Page-Get', API_Views.LegalPageViewSet, basename='Legal-Page')


# router.register('ExpertTaskCounting', API_Views.ExpertTaskCountViewSet, basename='ExpertTaskCounting')
# router.register('update_online', API_Views.update_online, basename='update_online')


from homofix_app import views
urlpatterns = [
    
    re_path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path("",include('homofix_app.urls')),
    path("Support/",include('homofix_app.support_urls')),
    path("Technician/",include('homofix_app.technician_urls')),

    path('api/Login/',API_Views.LoginViewSet.as_view(),name="api_login"),
    path('api/create_booking/',API_Views.create_booking,name="create_booking"),
    path('api/create_booking/manually',API_Views.create_booking_manually,name="create_booking_manually"),
    path('Demo/api/Login/',API_Views.LoginAPI.as_view(),name="demo_login"),
    path('api/Send/Otp/',API_Views.CustomerLoginViewSet.as_view(),name="api_customer_login"),
    path('api/Verify/otp/',API_Views.CustomerVerifyOtp.as_view(),name="verify_otp"),
    path('api/Custom/Login/',API_Views.CustomerLoginAPI.as_view(),name="customer_login"),
    
    path('api/',include(router.urls),name="api"),
    path('api/RechargeHistory/Post/',API_Views.post_rechargeHistory,name="recharge_history"),
    path('api/RechargeHistory/GET/',API_Views.get_RechargeHistory,name="recharge_history_get"),
    path('api/Wallet/GET/',API_Views.get_Wallet,name="get_Wallet"),
    path('api/Wallet/History/GET/',API_Views.get_Wallet_History,name="get_Wallet_History"),
    path('api/Withdraw/Request/Post/',API_Views.post_withdraw_req,name="post_withdraw_req"),
    path('api/Withdraw/Request/Get/',API_Views.get_Withdraw_Req,name="get_Withdraw_Req"),
    path('api/Task/Counting/Get/',API_Views.ExpertTaskCountViewSet,name="get_task_counting"),
    path('api/CustomerLogin/',API_Views.CustomerLogin.as_view(),name="CustomerLogin"),
    path('api/Addons/Delete',API_Views.addonsDelete.as_view(),name="addons_delete"),
    path('api/Invoice/',API_Views.generate_invoice_pdf,name="invoice"),
    
    # path("404",views.Error404,name="404"),
    # path('api/Expert/AllLocation',API_Views.create_or_update_all_technician_location,name="create_or_update_all_technician_location")
    # path("api/hompageservice/",API_Views.homepgservice,name="homepageserv"),

    path('<str:title>/', API_Views.BlogByTitleViewSet.as_view({'get': 'retrieve'}), name='blog-detail'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'homofix_app.views.Error404' 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()    