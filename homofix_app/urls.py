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
    path('Accounts/Admin/Technician',HodViews.technician,name="technician"),
    path('Accounts/Admin/Product',HodViews.product,name="product"),
   

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



    