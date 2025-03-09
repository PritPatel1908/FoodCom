from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from food_com.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from food_com.EmailBackEnd import EmailBackEnd
from django.contrib import messages
import os

# Vendor Admin
# Vendor Dashboard
def vendor_dashbord(request):
    return render(request, 'Vendor/Home Profile/index.html')

# Logout
def logout(request):
    del request.session['vendor_account']
    django_logout(request)
    messages.warning(request, "You are logged out.")
    return redirect('index')

# Product
# Add product page
def add_product_page(request):
    sub_category = Sub_Category.objects.all()
    context = {
        'sub_category' : sub_category
    }
    return render(request, 'Vendor/Product/add-product.html', context)

# Add product in database
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_ingredients = request.POST.get('product_ingredients')
        product_price = request.POST.get('product_price')
        product_old_price = request.POST.get('product_old_price')
        product_quantity = request.POST.get('product_quantity')
        sub_category_id = request.POST.get('sub_category_id')
        product_tags = request.POST.get('product_tags')
        product_img = request.FILES.get('product_img')
        file_data = request.FILES.getlist('product_imgs')

        if Product.objects.filter(product_name=product_name).exists():
            return JsonResponse({'message': 'Enter Another Product Name Because This Name Is Already Exist...'})
        else:
            product = Product(
                product_name = product_name,
                product_description = product_description,
                product_ingredients = product_ingredients,
                product_price = product_price,
                product_old_price = product_old_price,
                product_quantity = product_quantity,
                sub_category_id = sub_category_id,
                tags = product_tags,
                product_img = product_img,
                vendor_id = request.user.vendor_id
            )
            product.save()

            for file in file_data:
                product_images = Product_Images(
                    product_images = file,
                    product_id = product.product_id
                )
                product_images.save()

            return JsonResponse({'status': 200, 'message': 'Your product is added...'})
    return redirect(add_product_page)

# Manage product
def manage_product(request):
    # products = Product.objects.all().order_by('-date') this is show descending order
    products = Product.objects.all().order_by('date') #this is show ascending order
    context = {
        'products' : products
    }
    return render(request, 'Vendor/Product/manage-product.html', context)

# Edit product
def edit_product(request, product_id):
    products = Product.objects.get(product_id = product_id)
    sub_category = Sub_Category.objects.all()
    context = {
        'product' : products,
        'sub_category' : sub_category
    }
    return render(request, 'Vendor/Product/edit-product.html', context)

# Update product
def update_product(request, product_id):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_ingredients = request.POST.get('product_ingredients')
        product_price = request.POST.get('product_price')
        product_old_price = request.POST.get('product_old_price')
        product_quantity = request.POST.get('product_quantity')
        sub_category_id = request.POST.get('sub_category_id')
        product_tags = request.POST.get('product_tags')
        product_image = request.POST.get('product_image')
        product_img = request.FILES.get('product_img')

        product = Product.objects.get(product_id = product_id)
        sub_category = Sub_Category.objects.all()

        if product.product_name != product_name:
            product.product_name = product_name

        if product.product_description != product_description:
            product.product_description = product_description
            
        if product.product_ingredients != product_ingredients:
            product.product_ingredients = product_ingredients
            
        if product.product_price != product_price:
            product.product_price = product_price
            
        if product.product_old_price != product_old_price:
            product.product_old_price = product_old_price
            
        if product.product_quantity != product_quantity:
            product.product_quantity = product_quantity
            
        if product.sub_category_id != sub_category_id:
            product.sub_category_id = sub_category_id

        if product.tags != product_tags:
            product.tags = product_tags
            
        if product_img != product_image:
            if product_img != None:
                product.product_img = product_img
        product.save()

        context = {
            'product' : product,
            'sub_category' : sub_category
        }

        return JsonResponse({'status': 200, 'message': 'Your product is updated...'})
    return render(request, 'Vendor/Product/edit-product.html',context)

# Delete product
def delete_product(request, product_id):
    if request.method == 'POST':
        products = Product.objects.all()
        context = {
            'products' : products
        }

        product = Product.objects.get(product_id=product_id)
        product.delete()
        return JsonResponse({'status': 200, 'message': 'Your product is deleted...'})
    return render(request, 'Vendor/Product/manage-product.html', context)

# Categories
# Add category page
def add_category_page(request):
    return render(request, 'Vendor/Category/add-category.html')

# Add category in database
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_img = request.FILES.get('category_img')

        if Category.objects.filter(category_name=category_name).exists():
            return JsonResponse({'message': 'Enter Another Category Name Because This Name Is Already Exist...'})
        else:
            category = Category(
                category_name = category_name,
                category_img = category_img,
            )
            category.save()
            return JsonResponse({'status': 200, 'message': 'Your category is added...'})
    return redirect(add_category_page)

# Manage category
def manage_category(request):
    # category = Category.objects.all().order_by('-date') this is show descending order
    categories = Category.objects.all().order_by('date') #this is show ascending order
    context = {
        'categories' : categories
    }
    return render(request, 'Vendor/Category/manage-category.html', context)

# Edit Category
def edit_category(request, category_id):
    category = Category.objects.get(category_id = category_id)
    context = {
        'category' : category
    }
    return render(request, 'Vendor/Category/edit-category.html', context)

# Update product
def update_category(request, category_id):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_image = request.POST.get('category_image')
        category_img = request.FILES.get('category_img')

        category = Category.objects.get(category_id = category_id)

        if category.category_name != category_name:
            category.category_name = category_name
            
        if category_img != category_image:
            if category_img != None:
                category.category_img = category_img
        category.save()

        context = {
            'category' : category
        }

        return JsonResponse({'status': 200, 'message': 'Your category is updated...'})
    return render(request, 'Vendor/Product/edit-category.html',context)

# Delete category
def delete_category(request, category_id):
    if request.method == 'POST':
        categories = Category.objects.all().order_by('date') #this is show ascending order
        context = {
            'categories' : categories
        }

        category = Category.objects.get(category_id=category_id)
        category.delete()
        return JsonResponse({'status': 200, 'message': 'Your category is deleted...'})
    return render(request, 'Vendor/Category/manage-category.html', context)

# Sub category
# Add subcategory page
def add_subcategory_page(request):
    category = Category.objects.all()
    context = {
        'category' : category
    }
    return render(request, 'Vendor/Sub Category/add-subcategory.html', context)

# Add category in database
def add_subcategory(request):
    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        category_id = request.POST.get('category_id')
        subcategory_img = request.FILES.get('subcategory_img')

        if Sub_Category.objects.filter(subcategory_name=subcategory_name).exists():
            return JsonResponse({'message': 'Enter Another Sub Category Name Because This Name Is Already Exist...'})
        else:
            sub_category = Sub_Category(
                subcategory_name = subcategory_name,
                category_id = category_id,
                subcategory_img = subcategory_img,
            )
            sub_category.save()
            return JsonResponse({'status': 200, 'message': 'Your subcategory is added...'})
    return redirect(add_subcategory_page)

# Manage category
def manage_subcategory(request):
    # category = Category.objects.all().order_by('-date') this is show descending order
    sub_categories = Sub_Category.objects.all().order_by('date') #this is show ascending order
    context = {
        'sub_categories' : sub_categories
    }
    return render(request, 'Vendor/Sub Category/manage-subcategory.html', context)

# Edit Sub Category
def edit_subcategory(request, subcategory_id):
    sub_category = Sub_Category.objects.get(subcategory_id = subcategory_id)
    category = Category.objects.all()
    context = {
        'sub_category' : sub_category,
        'category' : category
    }
    return render(request, 'Vendor/Sub Category/edit-subcategory.html', context)

# Update sub category
def update_subcategory(request, subcategory_id):
    if request.method == 'POST':
        subcategory_name = request.POST.get('subcategory_name')
        category_id = request.POST.get('category_id')
        subcategory_image = request.POST.get('subcategory_image')
        subcategory_img = request.FILES.get('subcategory_img')

        print(subcategory_image,subcategory_img)
        sub_category = Sub_Category.objects.get(subcategory_id = subcategory_id)

        if sub_category.subcategory_name != subcategory_name:
            sub_category.subcategory_name = subcategory_name

        if sub_category.category_id != category_id:
            sub_category.category_id = category_id
            
        if subcategory_img != subcategory_image:
            if subcategory_img != None:
                sub_category.subcategory_img = subcategory_img
        sub_category.save()

        context = {
            'sub_category' : sub_category
        }

        return JsonResponse({'status': 200, 'message': 'Your sub category is updated...'})
    return render(request, 'Vendor/Sub Category/edit-subcategory.html',context)

# Delete sub category
def delete_subcategory(request, subcategory_id):
    if request.method == 'POST':
        sub_categories = Sub_Category.objects.all().order_by('date') #this is show ascending order
        context = {
            'sub_categories' : sub_categories
        }

        sub_category = Sub_Category.objects.get(subcategory_id=subcategory_id)
        sub_category.delete()
        return JsonResponse({'status': 200, 'message': 'Your sub category is deleted...'})
    return render(request, 'Vendor/Sub Category/manage-subcategory.html', context)

# Vendor profile page
def vendor_profile_page(request):
    vendor = Vendor.objects.get(user_id = request.user)
    context = {
        'vendor' : vendor
    }
    return render(request, 'Vendor/Profile/vendor-account-profile.html', context)

# Update basic profile
def update_basic_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        no_street_line = request.POST.get('no_street_line')
        pincode = request.POST.get('pincode')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        profile_image = request.POST.get('profile_image')
        profile_pic = request.FILES.get('profile_pic')

        user = Users.objects.get(user_id = request.user.user_id)

        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if phone != '':
            user.phone = phone
        if no_street_line != '':
            user.no_street_line = no_street_line
        if pincode != '':
            user.pincode = pincode
        if dob != '':
            user.dob = dob
        if gender != '':
            user.gender = gender
        if profile_pic != profile_image:
            if profile_pic != None:
                user.profile_pic = profile_pic
        user.save()

        vendor = Vendor.objects.get(user_id = request.user)
        context = {
            'vendor' : vendor
        }
        return JsonResponse({'status': 200, 'message': 'Your profile basic details is changed...'})
    return render(request, 'Vendor/Profile/vendor-account-profile.html', context)
    
# Update vendor profile
def update_vendor_profile(request):
    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')
        vendor_description = request.POST.get('vendor_description')
        vendor_address = request.POST.get('vendor_address')
        vendor_phone = request.POST.get('vendor_phone')
        shipping_on_time = request.POST.get('shipping_on_time')
        vendor_image = request.POST.get('vendor_image')
        vendor_img = request.FILES.get('vendor_img')

        vendor = Vendor.objects.get(user_id = request.user)

        if vendor_name != '':
            vendor.vendor_name = vendor_name
        if vendor_description != '':
            vendor.vendor_description = vendor_description
        if vendor_address != '':
            vendor.vendor_address = vendor_address
        if vendor_phone != '':
            vendor.vendor_phone = vendor_phone
        if shipping_on_time != '':
            vendor.shipping_on_time = shipping_on_time
        if vendor_img != vendor_image:
            if vendor_img != None:
                vendor.vendor_img = vendor_img
        vendor.save()

        context = {
            'vendor' : vendor
        }
        return JsonResponse({'status': 200, 'message': 'Your vendor profile is changed...'})
    return render(request, 'Vendor/Profile/vendor-account-profile.html', context)

# Order
# Manage order
def manage_order(request):
    orders = Order.objects.all().order_by('order_date') #this is show ascending order
    context = {
        'orders' : orders
    }
    return render(request, 'Vendor/Order/manage-order.html', context)

def get_order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    order_details = OrderDetails.objects.filter(order=order).values(
        "invoice_no", "product_status", "item", "item_id", "qty", "price", "total"
    )

    data = {
        "order_id": order.id,
        "user": order.user.username,
        "email": order.user.email,
        "price": order.price,
        "status": order.product_status,
        "date": order.order_date,
        "details": list(order_details),
    }

    return JsonResponse(data)

def update_order_status(request, order_id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id)
            new_status = request.POST.get("order_status")
            order.product_status = new_status
            order.save()
            return JsonResponse({"message": "Order status updated successfully!"}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)