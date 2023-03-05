
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
    path('Support/Task/Assign', SupportViews.support_Task_assign, name='support_Task_assign'),
    path('Support/Booking/List_of_expert/<int:id>', SupportViews.support_List_of_expert, name='support_List_of_expert'),
    path('Support/List/Task', SupportViews.support_list_of_task, name='support_list_of_task'),
    path('Support/Order/Cancel', SupportViews.order_cancel, name='order_cancel'),
    
#    ------------------------------ testing for request session --------------------- 

    path('myView/', SupportViews.myView, name='myView'),
    path('another_view/', SupportViews.another_view, name='another_view'),


]
