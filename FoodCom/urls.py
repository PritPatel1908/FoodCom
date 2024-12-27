"""
URL configuration for SUPERSTOREHUB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from food_com import views, admin_views, user_views, vendor_views

urlpatterns = [
    # Admin
    # Admin dashbord
    path('admin', admin_views.admin_dashbord, name="admin"),

    # Products
    path('admin/add_product_page', admin_views.add_product_page, name="add_product_page"),
    path('admin/add_product', admin_views.add_product, name="add_product"),
    path('admin/manage_product', admin_views.manage_product, name="manage_product"),
    path('admin/edit_product/<str:product_id>', admin_views.edit_product, name="edit_product"),
    path('admin/edit_product/<str:product_id>/update_product', admin_views.update_product, name="update_product"),
    path('admin/delete_product/<str:product_id>', admin_views.delete_product, name="delete_product"),

    # Categories
    path('admin/add_category_page', admin_views.add_category_page, name="add_category_page"),
    path('admin/add_category', admin_views.add_category, name="add_category"),
    path('admin/manage_category', admin_views.manage_category, name="manage_category"),
    path('admin/edit_category/<str:category_id>', admin_views.edit_category, name="edit_category"),
    path('admin/edit_category/<str:category_id>/update_category', admin_views.update_category, name="update_category"),
    path('admin/delete_category/<str:category_id>', admin_views.delete_category, name="delete_category"),

    # Subcategory
    path('admin/add_subcategory_page', admin_views.add_subcategory_page, name="add_subcategory_page"),
    path('admin/add_subcategory', admin_views.add_subcategory, name="add_subcategory"),
    path('admin/manage_subcategory', admin_views.manage_subcategory, name="manage_subcategory"),
    path('admin/edit_subcategory/<str:subcategory_id>', admin_views.edit_subcategory, name="edit_subcategory"),
    path('admin/edit_subcategory/<str:subcategory_id>/update_subcategory', admin_views.update_subcategory, name="update_subcategory"),
    path('admin/delete_subcategory/<str:subcategory_id>', admin_views.delete_subcategory, name="delete_subcategory"),

    # Vendor Account Request
    path('admin/manage_vendor_request_page', admin_views.manage_vendor_request_page, name="manage_vendor_request_page"),
    path('admin/add_manual_vendor_page', admin_views.add_manual_vendor_page, name="add_manual_vendor_page"),
    path('admin/add_vendor', admin_views.add_vendor, name="add_vendor"),
    path('admin/vendor_request_approve/<str:vendor_account_request_id>', admin_views.vendor_request_approve, name="vendor_request_approve"),
    path('admin/vendor_request_reject/<str:vendor_account_request_id>', admin_views.vendor_request_reject, name="vendor_request_reject"),

    # User
    # Home Page Url (User / Visitor)
    path('', views.index, name='index'),
    path('index', views.index, name='index'),

    # Search
    path('search/', user_views.search_view, name='search'),

    # Filter
    path('filter_product/', user_views.filter_product, name='filter_product'),

    # Add rating and review
    path('add_review/<str:product_id>', user_views.add_review, name='add_review'),
    path('load_more/<str:product_id>', user_views.load_more, name='load_more'),

    # Get vendor account
    path('get_vendor_account', user_views.get_vendor_account, name='get_vendor_account'),
    path('get_vendor_account_request', user_views.get_vendor_account_request, name='get_vendor_account_request'),

    # Vendor list and detail
    path('vendor_list', user_views.vendor_list, name='vendor_list'),
    path('vendor_detail/<str:vendor_id>', user_views.vendor_detail, name='vendor_detail'),

    # Product
    # All product list
    path('products', user_views.product_list, name='products'),
    path('product_detail/<str:product_id>', user_views.product_detail, name='product_detail'),
    path('tags_product_list/<str:tag>', user_views.tags_product_list, name='tags_product_list'),
    # Add / Remove cart product to all page
    path('add-to-cart-product-detail', user_views.add_to_cart_product_detail, name='add-to-cart-product-detail'),

    # All category list
    path('category', user_views.category_list, name='categories'),

    # Category to Sub Category list
    path('category_subcategory/<str:category_id>', user_views.category_subcategory_list, name='category_subcategories'),
    
    # Sub Category to Product list
    path('sub_category_product/<str:subcategory_id>', user_views.subcategory_product_list, name='sub_category_products'),

    # Accounts
    path('account_page', user_views.account_page, name='account_page'),

    # Vendor
    # Vendor dashbord
    path('vendor', vendor_views.vendor_dashbord, name="vendor"),

    # Vendor logout
    path('vendor_logout', vendor_views.logout, name='vendor_logout'),
    
    # Vendor account profile
    path('vendor/vendor_profile_page', vendor_views.vendor_profile_page, name="vendor_profile_page"),
    
    # Update basic profile
    path('vendor/update_basic_profile', vendor_views.update_basic_profile, name="update_basic_profile"),
    
    # Update vendor profile
    path('vendor/update_vendor_profile', vendor_views.update_vendor_profile, name="update_vendor_profile"),

    # Products
    path('vendor/add_product_page', vendor_views.add_product_page, name="vendor_add_product_page"),
    path('vendor/add_product', vendor_views.add_product, name="vendor_add_product"),
    path('vendor/manage_product', vendor_views.manage_product, name="vendor_manage_product"),
    path('vendor/edit_product/<str:product_id>', vendor_views.edit_product, name="vendor_edit_product"),
    path('vendor/edit_product/<str:product_id>/update_product', vendor_views.update_product, name="vendor_update_product"),
    path('vendor/delete_product/<str:product_id>', vendor_views.delete_product, name="vendor_delete_product"),

    # Categories
    path('vendor/add_category_page', vendor_views.add_category_page, name="vendor_add_category_page"),
    path('vendor/add_category', vendor_views.add_category, name="vendor_add_category"),
    path('vendor/manage_category', vendor_views.manage_category, name="vendor_manage_category"),
    path('vendor/edit_category/<str:category_id>', vendor_views.edit_category, name="vendor_edit_category"),
    path('vendor/edit_category/<str:category_id>/update_category', vendor_views.update_category, name="vendor_update_category"),
    path('vendor/delete_category/<str:category_id>', vendor_views.delete_category, name="vendor_delete_category"),

    # Subcategory
    path('vendor/add_subcategory_page', vendor_views.add_subcategory_page, name="vendor_add_subcategory_page"),
    path('vendor/add_subcategory', vendor_views.add_subcategory, name="vendor_add_subcategory"),
    path('vendor/manage_subcategory', vendor_views.manage_subcategory, name="vendor_manage_subcategory"),
    path('vendor/edit_subcategory/<str:subcategory_id>', vendor_views.edit_subcategory, name="vendor_edit_subcategory"),
    path('vendor/edit_subcategory/<str:subcategory_id>/update_subcategory', vendor_views.update_subcategory, name="vendor_update_subcategory"),
    path('vendor/delete_subcategory/<str:subcategory_id>', vendor_views.delete_subcategory, name="vendor_delete_subcategory"),

    # For all account
    # Login Existing Account (Sign-In)
    path('signin_page', views.signin_page, name='signin_page'),
    path('signin', views.signin, name='signin'),

    # Create New Account (Sign-Up)
    path('signup_page', views.signup_page, name='signup_page'),
    path('signup', views.signup, name='signup'),

    # Create New Account (Sign-Up)
    path('forgot_password_page', views.forgot_password_page, name='forgot_password_page'),
    path('check_forgot_password_email', views.check_forgot_password_email, name='check_forgot_password_email'),
    path('send_otp', views.send_otp, name='send_otp'),
    path('re_send_otp', views.re_send_otp, name='re_send_otp'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('clear_otp', views.clear_otp, name='clear_otp'),
    path('forgot_password', views.forgot_password, name='forgot_password'),

    # Logout
    path('logout', views.logout, name='logout'),
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
