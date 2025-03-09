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
import random
from django.db.models import Count,Avg

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return render(request, 'Admin/Home Profile/index.html')
        else:
            check_account = request.session.get('vendor_account')
            if check_account == True:
                return render(request, 'Vendor/Home Profile/index.html')
            else:
                products = Product.objects.all().order_by('date')
                categories = Category.objects.all().order_by('date')
                sub_categories = Sub_Category.objects.all().order_by('date')

                cart_total_amount = 0
                if 'cart_data_obj' in request.session:
                    for product_id, item in request.session['cart_data_obj'].items():
                        cart_total_amount += int(item['product_quantity']) * float(item['product_price'])
                
                if 'cart_data_obj' not in request.session:
                    request.session['cart_data_obj'] = {}

                top_selling_products = OrderDetails.objects.values('item').annotate(total_sales=Count('item')).order_by('-total_sales')
                top_selling_products_list = []
                top_selling_products_rating = []
                for items in top_selling_products:
                    top_selling_products_list.extend(Product.objects.filter(product_name=items['item']))

                trending_products = Product_Review.objects.values('product').annotate(total_product_rating=Count('product_rating')).order_by('-total_product_rating')
                trending_products_list = []
                trending_products_rating = []
                for items in trending_products:
                    trending_products_list.extend(Product.objects.filter(product_id=items['product']))

                new_products = Product.objects.all().order_by('-date')[:5]

                context = {
                    'products': products,
                    'categories' : categories,
                    'sub_categories' : sub_categories,
                    'cart_data' : request.session['cart_data_obj'],
                    'total_cart_items' : len(request.session['cart_data_obj']),
                    'cart_total_amount':cart_total_amount,
                    'top_selling_products' : top_selling_products_list,
                    'trending_products' : trending_products_list,
                    'new_products' : new_products,
                }
                return render(request, 'User/index.html', context)
    else:
        products = Product.objects.all().order_by('date')
        categories = Category.objects.all().order_by('date')
        context = {
            'products': products,
            'categories' : categories
        }
        return render(request, 'User/index.html', context)

# Signup
# Signup Page
def signup_page(request):
    return render(request, 'signup.html')
    
# Signup 
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        try:
            user = Users.objects.get(email = email)
            if user.username == username:
                return JsonResponse({'status': 400, 'error': 'Your username is already used try new username.'})
            if user.email == email:
                return JsonResponse({'status': 400, 'error': 'Your email is already used try new email.'})
        except Users.DoesNotExist:
            if len(password) < 8:
                return JsonResponse({'status': 400, 'error': 'Password must be at least 8 characters long.'})

            if password != cpassword:
                return JsonResponse({'status': 400, 'error': 'Password and Confirm Password do not match.'})
        
            user = Users(
                username = username,
                email = email,
                password = make_password(password),
                user_type = 2
            )
            user.save()

            return JsonResponse({'status': 200})
    return redirect('signup_page')

# Signin
# Signin Page
def signin_page(request):
    return render(request, 'signin.html')

# Signin
def signin(request):
    if request.method == 'POST':
        usernameoremail=request.POST.get('usernameoremail')
        password=request.POST.get('password')

        if len(password) < 8:
            return JsonResponse({'status': 400, 'error': 'Password must be at least 8 characters long.'})

        user = EmailBackEnd.authenticate(request, usernameoremail, password)

        if user is not None: 
            login(request, user)
            user_type = user.user_type
            if user_type == 1:
                return JsonResponse({'status': 200})
            elif user_type == 2:
                if '@' in usernameoremail:
                    messages.success(request, "You are logged in.")
                    return JsonResponse({'status': 201})
                elif 'ven' in usernameoremail:
                    request.session['vendor_account'] = True
                    return JsonResponse({'status': 202})
                else:
                    messages.success(request, "You are logged in.")
                    return JsonResponse({'status': 201})
            else:
                return JsonResponse({'status': 400, 'error': 'You have not created account so first create account !'})
        else:
            return JsonResponse({'status': 400, 'error': 'Email / Username or Password are invalid !!'})
    return redirect('signin_page')

# Forgot Password
# Forgot Password Page
def forgot_password_page(request):
    return render(request, 'forgot_password.html')

# Check Forgot Password Email
def check_forgot_password_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Users.objects.get(email = email)
            return JsonResponse({'status': 200, 'email' : user.email})
        except Users.DoesNotExist:
            return JsonResponse({'status': 400, 'error': 'Email is not registered !'})
        
# Send Otp
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = random.randint(111111,999999)

        if email == '':
            return JsonResponse({'email':email, 'error':'Your email is not found try again !'})
        else:
            try:
                user = Users.objects.get(email = email)
                user.otp = otp
                user.save()
                send_mail(
                    'Message To FOOD.COM',
                    'FOOD.COM is send OTP for your request of forgot password your OTP is - '+str(otp),
                    'foodcom0750@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return JsonResponse({'status': 200, 'email':email})
            except Users.DoesNotExist:
                return JsonResponse({'email':email, 'error':'Your email is is not match try again with valid email!'})
    return render(request, 'forgot_password.html')

# Re-Send OTP
def re_send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('aftergetemail')
        otp = random.randint(111111,999999)

        user = Users.objects.get(email = email)
        user.otp = otp
        user.save()

        send_mail(
            'Message To FOOD.COM',
            'FOOD.COM is resend OTP for your request of resend otp your OTP is - '+str(otp),
            'foodcom0750@gmail.com',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'status': 200, 'email':email})
    return render(request, 'forgot_password.html')

# Clear Otp
def clear_otp(request):
    if request.method == 'POST':
        email = request.POST.get('aftergetemail')

        user = Users.objects.get(email = email)

        if user:
            user.otp = 0
            user.save()
        else:
            print('error')

    return render(request, 'forgot_password.html')

# Verify OTP
def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('aftergetemail')
        otp = request.POST.get('otp')

        if otp == '':
            return JsonResponse({'email':email, 'error':'Your otp is not found try again !'})
        else:
            try:
                user = Users.objects.get(email = email)
                if str(user.otp) == otp:
                    user.otp = 0
                    user.save()
                    return JsonResponse({'status': 200, 'email':email})
                else:
                    return JsonResponse({'email':email, 'error':'Your otp is not match try again with correct otp !'})
            except Users.DoesNotExist:
                return JsonResponse({'email':email, 'error':'Your email is is not match try again with valid email!'})

    return render(request, 'forgot_password.html')

# Forgot Password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('passwordemail')
        passw = request.POST.get('new_password')
        cpassw = request.POST.get('new_confirm_password')
        password = make_password(passw)

        if passw == cpassw:
            try:
                user = Users.objects.get(email = email)
                if user:
                    user.password = password
                    user.save()
                return JsonResponse({'status': 200,})
            except Users.DoesNotExist:
                return JsonResponse({'email':email, 'error':'Your password and confirm password is not match try again!'})
        else:
            return JsonResponse({'email':email, 'error':'Your password and confirm password is not match try again!'})
    return render(request, 'forgot-password.html')

# Logout
def logout(request):
    django_logout(request)
    messages.warning(request, "You are logged out.")
    return redirect('index')

def favicon(request):
    return HttpResponse("", content_type="image/x-icon")