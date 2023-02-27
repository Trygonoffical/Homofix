
from django.urls import path
from homofix_app import views,SupportViews

urlpatterns = [
    path('', SupportViews.dashboard,name="support_dashboard"),
    path('Support/Profile', SupportViews.support_profile,name="support_profile"),
    path('Support/Update/Profile', SupportViews.support_profile_update,name="support_profile_update"),
    path('Support/Orders/', SupportViews.support_orders,name="support_orders"),
    path('Support/Orders/Otp', SupportViews.support_otp,name="support_otp"),
    path('Support/Orders/Verify/Otp', SupportViews.support_verify_otp,name="support_verify_otp"),
    path('support_booking/', SupportViews.support_booking, name='support_booking'),
    path('reschedule_booking/', SupportViews.reschedule_booking, name='reschedule_booking'),
    path('cancel_booking/<int:booking_id>', SupportViews.cancel_booking, name='cancel_booking'),
    
#    ------------------------------ testing for request session --------------------- 

    path('myView/', SupportViews.myView, name='myView'),
    path('another_view/', SupportViews.another_view, name='another_view'),


]
