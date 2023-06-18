"""
URL configuration for MMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from account_mgmt.views import * 
from product_mgmt.views import *

urlpatterns = [

    path('admin/', admin.site.urls),
    path('seller-registration/', seller_registration, name='seller-registration'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('login/', login_view, name='login'),
    path('logout/', CustomLogOutView.as_view(), name='logout'),
    path('home/',home, name='home'),
    path('profile<int:user_id>/',seller_profile, name='profile'),
    path('change-photo/',change_profile_photo, name='change-photo'),
    path('edit-bio/',edit_bio, name='edit-bio'),
    path('verify-account/',verify_account, name='verify-account'),
    path('',home, name='home'),

    #admins
    path('admin-signup/',admin_registration, name='admin-signup'),
    path('admin-login/', admin_login_view, name='admin-login'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('pending-kyc/', pending_kyc_verification, name='pending-kyc'),
    path('verify-seller<int:user_id>/', verify_seller, name='verify-seller'),
    path('approve-seller<int:user_id>/', approve_seller, name='approve-seller'),
    path('decline-seller<int:user_id>/', decline_seller, name='decline-seller'),

    #Product related
    path('add-store/', add_store, name='add-store'),
    path('store-list<int:user_id>/', store_list, name='store-list'),
    path('add-product/', upload_product, name='add-product'),
    path('search/', search, name='search'),
    path('product-info<int:product_id>/', product_info, name='product-info'),
    path('edit-product-info<int:product_id>/', edit_product_info, name='edit-product-info'),
    path('delete-product<int:product_id>/', delete_product, name='delete-product'),
    path('how-to-get-link/', how_to_get_gmap_link, name='how-to-get-link'),








] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)