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
from django.db.models import Count, Avg
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required

# Vendor
# Get vendor account
def get_vendor_account(request):
    get_vendor_account_query = Vendor_Account_Request.objects.filter(user = request.user).first()
    vendor = Vendor.objects.filter(user = request.user).first()
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'get_vendor_account_query' : get_vendor_account_query,
        'vendor' : vendor,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/get-vendor-account.html', context)

# Get vendor account request
def get_vendor_account_request(request):
    if request.method == 'POST':
        vendor_account_request = Vendor_Account_Request(
            user = request.user
        )
        vendor_account_request.save()
        return JsonResponse({'status': 200, 'message': 'Your vendor account get request is successfully send...'})
    return render(request, 'User/get-vendor-account.html')

# Vendor list
def vendor_list(request):
    vendors = Vendor.objects.all().order_by('date')

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'vendors' : vendors,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/vendor-list.html', context)
    
# Vendor detail
def vendor_detail(request, vendor_id):
    vendor = Vendor.objects.get(vendor_id = vendor_id)
    vendor_products = Product.objects.filter(vendor_id = vendor_id).order_by('date')
    categories = Category.objects.all().order_by('date')

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'vendor' : vendor,
        'vendor_products' : vendor_products,
        'categories' : categories,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/vendor-detail.html', context)

# Product
# Product list
def product_list(request):
    products = Product.objects.all().order_by('date')

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'products': products,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/product-list.html', context)

# Product detail
def product_detail(request, product_id):
    product = Product.objects.get(product_id = product_id)
    related_products = Product.objects.filter(sub_category = product.sub_category).exclude(product_id = product_id)[:4]
    products_images = Product_Images.objects.filter(product_id = product_id)

    reviews = Product_Review.objects.filter(product = product).order_by('-product_review_date')
    average_rating = Product_Review.objects.filter(product = product).aggregate(rating=Avg('product_rating'))

    total_review = reviews.count()

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'product': product,
        'product_images' : products_images,
        'related_products' : related_products,
        'reviews' : reviews,
        'average_rating' : average_rating,
        'total_review': total_review,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    
    if total_review > 0:
        context['one_star_percentage'] = reviews.filter(product_rating=1).count() / total_review * 100
        context['two_star_percentage'] = reviews.filter(product_rating=2).count() / total_review * 100
        context['three_star_percentage'] = reviews.filter(product_rating=3).count() / total_review * 100
        context['four_star_percentage'] = reviews.filter(product_rating=4).count() / total_review * 100
        context['five_star_percentage'] = reviews.filter(product_rating=5).count() / total_review * 100

    tags = context['product'].tags.split(',') if context['product'] and context['product'].tags else []
    context['tags'] = [tag.strip() for tag in tags]
    return render(request, 'User/product-detail.html', context)

# Product tags list
def tags_product_list(request, tag):
    tagged_products = Product.objects.filter(tags__contains=tag)
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'tagged_products' : tagged_products,
        'tag' : tag,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/tagged-product-list.html', context)

# Product add review
def add_review(request, product_id):
    if request.method == 'POST':
        ratingValue = request.POST.get('ratingValue')
        product_review_message = request.POST.get('product_review_message')
        product_id = request.POST.get('product_id')

        product_review = Product_Review(
            product_review_message = product_review_message,
            product_rating = ratingValue,
            product_id = product_id,
            user = request.user
        )
        product_review.save()

        return JsonResponse({'status': 200, 'message': 'Your review is successfully submited...'})
    return render(request, 'User/product-detail.html')

# Product Load more review
def load_more(request, product_id):
    total_review = int(request.GET.get('total_review'))
    limit = 2
    review_obj = list(Product_Review.objects.filter(product_id = product_id).select_related('user').values('product_review_id', 'product_review_message', 'product_review_date', 'product_rating', 'user__profile_pic', 'user__first_name', 'user__last_name').order_by('-product_review_date')[total_review:total_review+limit])
    data = {
        'review' : review_obj,
    }
    return JsonResponse(data=data)

# Categories
# Category list
def category_list(request):
    categories = Category.objects.all().order_by('date')
    sub_categories = Sub_Category.objects.all().order_by('date')

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'categories' : categories,
        'sub_categories' : sub_categories,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/category-list.html', context)
    
# Categoryoo sub category list
def category_subcategory_list(request, category_id):
    category = Category.objects.get(category_id = category_id)
    categories = Category.objects.all().order_by('date')
    sub_categories = Sub_Category.objects.filter(category = category).order_by('date')
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'category' : category,
        'categories' : categories,
        'sub_categories' : sub_categories,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/category-to-subcategory-list.html', context)
    
# Sub category to product list
def subcategory_product_list(request, subcategory_id):
    sub_category = Sub_Category.objects.get(subcategory_id = subcategory_id)
    products = Product.objects.filter(sub_category = sub_category).order_by('date')

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'sub_category' : sub_category,
        'products' : products,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/subcategory-to-product-list.html', context)

# Search
# Search product
def search_view(request):
    search = request.GET.get('s')
    products = Product.objects.filter(product_name__icontains=search).order_by('date')

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}

    context = {
        'products' : products,
        'search' : search,
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount
    }
    return render(request, 'User/search.html', context)

# Filter
# Filter product
def filter_product(request):
    sub_categories = request.GET.getlist('sub_category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.all().order_by('date').distinct()

    products = products.filter(product_price__gte=min_price)
    products = products.filter(product_price__lte=max_price)

    if len(sub_categories) > 0:
        products = products.filter(sub_category_id__in=sub_categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor_id__in=vendors).distinct()

    data = render_to_string("User/async/product-list.html", {"products" : products})
    data_count = render_to_string("User/async/product-count.html", {"products" : products})
    return JsonResponse({"data" : data, "data_count" : data_count})

# View
# Quick view for product
def quick_view(request, product_id):
    product = Product.objects.get(product_id = product_id)
    return render(request, 'User/async/quick_view_modal.html', {'product': product})

# Add / Remove cart to product detail page
def add_to_cart_product_detail(request):
    cart_product = {}
    cart_product[str(request.GET['product_id'])] = {
        'product_name' : request.GET['product_name'],
        'product_quantity' : request.GET['product_quantity'],
        'product_price' : request.GET['product_price'],
        'product_img' : request.GET['product_img'],
        'product_id' : request.GET['product_id']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['product_id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            if int(cart_data[str(request.GET['product_id'])]['product_quantity']) > 1:
                cart_data[str(request.GET['product_id'])]['product_quantity'] = int(cart_data[str(request.GET['product_id'])]['product_quantity']) - 1
                cart_data.update(cart_data)
                request.session['cart_data_obj'] = cart_data
                return JsonResponse({"status" : 401, "data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj'])})
            else:
                del cart_data[str(request.GET['product_id'])]
                request.session['cart_data_obj'] = cart_data
                request.session.modified = True
                return JsonResponse({"status" : 400, "data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj'])})
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            return JsonResponse({"status" : 200, "data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj'])})
    else:
        request.session['cart_data_obj'] = cart_product
        return JsonResponse({"status" : 200, "data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj'])})
    return JsonResponse({"data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj'])})

def cart_page(request):
    categories = Category.objects.all().order_by('date')
    sub_categories = Sub_Category.objects.all().order_by('date')
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])
        return render(request, 'User/cart.html', {"cart_data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj']), 'cart_total_amount' : cart_total_amount, 'categories' : categories, 'sub_categories' : sub_categories})
    else:
        messages.warning(request, "Your cart is empty...")
        return redirect("index")

def delete_to_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    context = render_to_string("User/async/cart-list.html", {"cart_data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj']), 'cart_total_amount' : cart_total_amount})
    return JsonResponse({"data" : context, 'total_cart_items' : len(request.session['cart_data_obj'])})

def update_to_cart(request):
    product_id = str(request.GET['id'])
    product_quantity = request.GET['product_quantity']

    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['product_quantity'] = product_quantity
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    context = render_to_string("User/async/cart-list.html", {"cart_data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj']), 'cart_total_amount' : cart_total_amount})
    return JsonResponse({"data" : context, 'total_cart_items' : len(request.session['cart_data_obj'])})

# Checkout
@login_required
def checkout_view(request):
    cart_total_amount = 0
    categories = Category.objects.all().order_by('date')
    sub_categories = Sub_Category.objects.all().order_by('date')
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
            request.session['cart_data_obj'] = {}
    return render(request, 'User/checkout.html', {"cart_data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj']), 'cart_total_amount' : cart_total_amount, 'categories' : categories, 'sub_categories' : sub_categories})

# Checkout
@login_required
def cod_order(request):
    cart_total_amount = 0
    total_amount = 0

    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['product_quantity']) * float(item['product_price'])
        
        order = Order.objects.create(
            user = request.user,
            price = total_amount,
            payment_status = 'cod'
        )

        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

            order_details = OrderDetails.objects.create(
                order = order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item = item['product_name'],
                item_id = product_id,
                qty = item['product_quantity'],
                price = item['product_price'],
                total = float(item['product_quantity']) * float(item['product_price'])
            )

    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}

    # host = request.get_host()
    # paypal_dict = {
    #     'business' : settings.PAYPAL_RECEIVER_EMAIL,
    #     'amount' : cart_total_amount,
    #     'item_name' : 'Order-Item-No' + str(order.id),
    #     'invoice' : 'Invoice-No' + str(order.id),
    #     'currency_code' : 'USD',
    #     'notify_url' : 'http://{}{}'.format(host, reverse('paypal-ipn')),
    #     'return_url' : 'http://{}{}'.format(host, reverse('payment_completed')),
    #     'cancel_url' : 'http://{}{}'.format(host, reverse('payment_failed'))
    # }

    # paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    return redirect('index')

# payment
# payment complete
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}
    return render(request, 'User/payment-completed.html', {"cart_data" : request.session['cart_data_obj'], 'total_cart_items' : len(request.session['cart_data_obj']), 'cart_total_amount' : cart_total_amount})

# payment complete
def payment_failed_view(request):
    return render(request, 'User/payment-failed.html')
    
# oredr details
def order_details(request, id):
    order = Order.objects.get(id = id)
    order_details = OrderDetails.objects.filter(order = order)
    for order_detail in order_details:
        try:
            order_detail.product = Product.objects.get(product_name=order_detail.item)
        except Product.DoesNotExist:
            order_detail.product = None  # Handle missing products gracefully

    return render(request, 'User/payment-completed.html', {
        "order": order,
        "order_details": order_details
    })

# Account
# Account page
def account_page(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['product_quantity']) * float(item['product_price'])

    if 'cart_data_obj' not in request.session:
        request.session['cart_data_obj'] = {}
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'cart_data' : request.session['cart_data_obj'],
        'total_cart_items' : len(request.session['cart_data_obj']),
        'cart_total_amount' : cart_total_amount,
        'orders' : orders
    }
    return render(request, 'User/account.html', context)

def order_tracking(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'User/order_tracking.html', {'order': order})

@login_required
@csrf_exempt
def update_user_details(request):
    if request.method == "POST":
        user = request.user

        # Basic User model fields
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.phone = request.POST.get("phone", user.phone)
        user.gender = request.POST.get("gender", user.gender)
        user.dob = request.POST.get("dob", user.dob)
        user.no_street_line = request.POST.get("no_street_line", user.no_street_line)
        user.city = request.POST.get("city", user.city)
        user.pincode = request.POST.get("pincode", user.pincode)
        user.state = request.POST.get("state", user.state)
        user.country = request.POST.get("country", user.country)

        user.save()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
