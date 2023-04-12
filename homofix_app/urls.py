from django.urls import path
from homofix_app import views,HodViews
from homofix_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    

    path('',views.login,name="login"),
    path('user/logout',views.logout_user,name="user_logout"),
    path("Accounts/Admin/Change/Password",HodViews.admin_reset_psw,name="admin_reset_psw"),
    path("Accounts/Admin/Dashboard/",HodViews.admin_dashboard,name="admin_dashboard"),
    path('Accounts/Admin/Add',HodViews.add_admin,name="add_admin"),
    path('Accounts/Admin/Edit/<int:id>',HodViews.edit_admin,name="edit_admin"),
    path('Accounts/Admin/List',HodViews.admin_list,name="admin_list"),
    path('Accounts/Admin/Profile',HodViews.admin_profile,name="admin_profile"),
    path('Accounts/Admin/Updata/Profile',HodViews.admin_update_profile,name="admin_update_profile"),
    path('Accounts/Admin/Category/',HodViews.category,name="category"),
    path('Add/Category',HodViews.add_category,name="add_category"),
    path('Category/Delete/<int:id>',HodViews.delete_Category,name="delete_Category"),
    path('Category/Edit/',HodViews.edit_Category,name="edit_Category"),

    path('Accounts/Admin/SubCategory/',HodViews.subcategory,name="subcategory"),
    path('Accounts/Admin/SubCategory/Edit',HodViews.edit_subcategory,name="edit_subcategory"),
    path('Accounts/Admin/SubCategory/Delete/<int:id>',HodViews.delete_subcategory,name="delete_subcategory"),
    path('get-subcategories/', HodViews.get_subcategories, name='get_subcategories'),
    path('get-products/', HodViews.get_products, name='get_products'),


# ----------------------------------------- Technician ------------------------- 

    path('Accounts/Admin/Technician',HodViews.technician,name="technician"),
    path('Accounts/Admin/ADD/Technician',HodViews.add_technician,name="add_technician"),
    path('Accounts/Admin/Technician/AddCategory',HodViews.technician_add_category,name="technician_add_category"),
    path('Accounts/Admin/Technician/Profile/<int:id>',HodViews.technician_edit_profile,name="technician_edit_profile"),
    path('Accounts/Admin/Technician/Edit',HodViews.edit_technician,name="edit_technician"),
    path('Accounts/Technician/Delete/<int:id>',HodViews.delete_technician,name="delete_technician"),
    path('Accounts/Technician/History/<int:id>',HodViews.technician_history,name="technician_history"),
    path('Accounts/Technician/Payment/History/<int:id>',HodViews.technician_payment_history,name="technician_payment_history"),
    # path('Accounts/Technician/ADD/Payment/History',HodViews.technician_add_payment_history,name="technician_add_payment_history"),
    path('Accounts/Admin/Product',HodViews.product,name="product"),
    path('Accounts/Admin/Product/Update',HodViews.update_product,name="update_product"),
    path('Accounts/Admin/Product/Delete/<int:id>',HodViews.delete_product,name="delete_product"),


    ########################## Addons ##################################
    
    path('Accounts/Admin/Addons',HodViews.addons,name="addons"),
    path('Accounts/Admin/Addons/Edit',HodViews.update_addons,name="update_addons"),
    path('Accounts/Admin/Addons/Delete/<int:id>',HodViews.delete_addons,name="delete_addons"),
    path('Accounts/Admin/Addons/Details/',HodViews.addons_details,name="addons_details"),



    ########################## Support ##################################

    path('Accounts/Admin/Support',HodViews.support,name="admin_support"),
    path('Accounts/Admin/Add/Support',HodViews.add_support,name="add_support"),
    path('Accounts/Admin/Support/Profile/<int:id>',HodViews.support_profile,name="support_profile"),
    path('Accounts/Admin/Support/Profile/Update/',HodViews.support_update_profile,name="support_update_profile"),
    path('Accounts/Admin/Support/Delete/<int:id>/',HodViews.delete_support,name="delete_support"),
    path('Accounts/Admin/Support/History/<int:id>/',HodViews.support_history,name="support_history"),
    

    ########################## FAQS ##################################
    path('Accounts/Admin/FAQ', HodViews.add_faq, name='add_faq'),
    path('Accounts/Admin/FAQ/Update', HodViews.update_add_faq, name='update_add_faq'),
    path('Accounts/Admin/FAQ/Delete/<int:id>/', HodViews.delete_faq, name='delete_faq'),

    ########################## Booking List ##################################
     path('Accounts/Admin/BookingList', HodViews.booking_list, name='booking_list'),
     path('Accounts/Admin/Reschudule', HodViews.admin_reschedule, name='admin_reschedule'),
     path('Accounts/Admin/cancel_booking/<int:booking_id>', HodViews.cancel_booking_byadmin, name='cancel_booking_byadmin'),
     path('Accounts/Admin/taskAssign/', HodViews.task_assign, name='task_assign'),
     path('Accounts/Admin/ListofTask/', HodViews.list_of_task, name='list_of_task'),
     path('Accounts/Admin/Booking/Listofcancel', HodViews.Listofcancel, name='Listofcancel'),


    ########################## Notification ##################################

    path('Accounts/Admin/Notification/NewExpert', HodViews.ListofNewExpert, name='ListofNewExpert'),
    
    ########################## Rebooking ##################################

    path('Accounts/Admin/Rebooking/', HodViews.Listofrebooking, name='Listofrebooking'),

    ########################## Contact Us ##################################
    path('Accounts/Admin/ContactUs/', HodViews.contactus, name='contact_us'),

    ########################## Job Enquiry ##################################
    path('Accounts/Admin/Job/Enquiry', HodViews.admin_job_enquiry, name='admin_job_enquiry'),

    ########################## Job Enquiry ##################################
    path('Accounts/Admin/Share/Percantage', HodViews.admin_share_percentage, name='admin_share_percentage'),
    path('Accounts/Admin/Share/List', HodViews.admin_share_list, name='admin_share_list'),


    ########################## Customer ##################################

    path('Accounts/Admin/Customer/List', HodViews.admin_customer_list, name='admin_customer_list'),
    path('Accounts/Admin/Customer/Edit/<int:id>', HodViews.admin_customer_edit, name='admin_customer_edit'),
    path('Accounts/Admin/Customer/History/<int:id>', HodViews.admin_customer_history, name='admin_customer_history'),

    ########################## Customer Payment Details ##################################
    path('Accounts/Admin/Customer/Payment/Details', HodViews.admin_customer_payment, name='admin_customer_payment'),
    



    # ------------------------------------- table amount total show dummy --------------- 
    # path('Accounts/Admin/Customer/Payment/Details', HodViews.admin_customer_payment, name='admin_customer_payment'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    