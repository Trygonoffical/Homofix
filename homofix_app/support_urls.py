
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
    path('Support/Task/Counting/<int:expert_id>/', SupportViews.support_task_counting, name='support_task_counting'),
    path('Support/Booking/Complete/', SupportViews.support_booking_complete, name='support_booking_complete'),
    path('Support/Booking/Rebooking/<int:task_id>', SupportViews.support_rebooking, name='support_rebooking'),
    path('Support/Booking/Rebooking/Details', SupportViews.support_rebooking_list, name='support_rebooking_list'),
    path('Support/Booking/Rebooking/Update/', SupportViews.support_rebooking_update, name='support_rebooking_update'),
    
#    ------------------------------ EXPERT --------------------- 
    path('Support/Expert/list_of_expert', SupportViews.support_list_of_expert, name='support_list_of_expert'),
    path('Support/Expert/add_expert', SupportViews.support_add_expert, name='support_add_expert'),
    path('Support/Expert/Edit/Profile/<int:id>',SupportViews.expert_edit_profile,name="expert_edit_profile"),


#    ------------------------------ Rebooking Product --------------------- 

    # path('Support/Expert/Rebooking/Product/<int:id>', SupportViews.support_rebooking_product, name='support_rebooking_product'),
    path('Support/Expert/Rebooking/Product/<int:task_id>', SupportViews.support_rebooking_product, name='support_rebooking_product'),




#    ------------------------------ testing for request session --------------------- 

    path('myView/', SupportViews.myView, name='myView'),
    path('another_view/', SupportViews.another_view, name='another_view'),


]
