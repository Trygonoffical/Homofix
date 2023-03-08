
from django.urls import path
from homofix_app import views,TechnicianViews

urlpatterns = [
    path('', TechnicianViews.dashboard,name="technician_dashboard"),
    path('Expert/Task/Assign', TechnicianViews.expert_task_assign,name="expert_task_assign"),
    path('update-booking-status/<int:booking_id>', TechnicianViews.update_booking_status, name='update_booking_status'),
    
   
]
