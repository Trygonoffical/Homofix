
from django.urls import path
from homofix_app import views,TechnicianViews

urlpatterns = [
    path('', TechnicianViews.dashboard,name="technician_dashboard"),
    path('Expert/Task/Assign', TechnicianViews.expert_task_assign,name="expert_task_assign"),
    path('update-booking-status/<int:booking_id>', TechnicianViews.update_booking_status, name='update_booking_status'),
    path('Expert/Rebooking/Rebooking-Details', TechnicianViews.expert_rebooking_Task,name="expert_rebooking_Task"),
    path('update-re-booking-status/<int:booking_id>', TechnicianViews.update_rebooking_status, name='update_rebooking_status'),
    
   
]
