from django.urls import path
from homofix_app import views,HodViews
from homofix_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    

    path('',views.login,name="login"),
    path('user/logout',views.logout_user,name="user_logout"),
    path("Accounts/Admin/Dashboard/",HodViews.admin_dashboard,name="admin_dashboard"),
    path('Accounts/Admin/Profile',HodViews.admin_profile,name="admin_profile"),
    path('Accounts/Admin/Updata/Profile',HodViews.admin_update_profile,name="admin_update_profile"),
    path('Accounts/Admin/Category/',HodViews.category,name="category"),
    path('Add/Category',HodViews.add_category,name="add_category"),
    path('Category/Delete/<int:id>',HodViews.delete_Category,name="delete_Category"),
    path('Category/Edit/',HodViews.edit_Category,name="edit_Category"),
    path('Accounts/Admin/Technician',HodViews.technician,name="technician"),
    path('Accounts/Admin/Technician/AddCategory',HodViews.technician_add_category,name="technician_add_category"),
    path('Accounts/Admin/Technician/Profile/<int:id>',HodViews.technician_edit_profile,name="technician_edit_profile"),
    path('Accounts/Admin/Technician/Edit',HodViews.edit_technician,name="edit_technician"),
    path('Accounts/Technician/Delete/<int:id>',HodViews.delete_technician,name="delete_technician"),
    path('Accounts/Admin/Product',HodViews.product,name="product"),
    path('Accounts/Admin/Product/Update',HodViews.update_product,name="update_product"),
    path('Accounts/Admin/Product/Delete/<int:id>',HodViews.delete_product,name="delete_product"),


    ########################## Addons ##################################
    path('Accounts/Admin/Addons',HodViews.addons,name="addons"),
    path('Accounts/Admin/Addons/Edit',HodViews.update_addons,name="update_addons"),
    path('Accounts/Admin/Addons/Delete/<int:id>',HodViews.delete_addons,name="delete_addons"),



    ########################## Support ##################################

    path('Accounts/Admin/Support',HodViews.support,name="admin_support"),
    path('Accounts/Admin/Add/Support',HodViews.add_support,name="add_support"),
    path('Accounts/Admin/Support/Profile/<int:id>',HodViews.support_profile,name="support_profile"),
    path('Accounts/Admin/Support/Profile/Update/',HodViews.support_update_profile,name="support_update_profile"),
    path('Accounts/Admin/Support/Delete/<int:id>/',HodViews.delete_support,name="delete_support"),
    

    ########################## FAQS ##################################
    path('Accounts/Admin/FAQ', HodViews.add_faq, name='add_faq'),

    ########################## Booking List ##################################
     path('Accounts/Admin/BookingList', HodViews.booking_list, name='booking_list'),
     path('Accounts/Admin/Reschudule', HodViews.admin_reschedule, name='admin_reschedule'),
     path('Accounts/Admin/cancel_booking/<int:booking_id>', HodViews.cancel_booking_byadmin, name='cancel_booking_byadmin'),
     path('Accounts/Admin/taskAssign/', HodViews.task_assign, name='task_assign'),
     path('Accounts/Admin/ListofTask/', HodViews.list_of_task, name='list_of_task'),
     path('Accounts/Admin/Booking/Listofcancel', HodViews.Listofcancel, name='Listofcancel'),


    ########################## Notification ##################################

    path('Accounts/Admin/Notification/NewExpert', HodViews.ListofNewExpert, name='ListofNewExpert'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    