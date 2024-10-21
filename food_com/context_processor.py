from food_com.models import *
from django.db.models import Count, Min, Max

def default(request):
    categories = Category.objects.all().order_by('date')
    sub_categories = Sub_Category.objects.all().order_by('date')
    vendors = Vendor.objects.all().order_by('date')
    address = Address.objects.filter(user_id = request.user).first()

    min_max_price = Product.objects.aggregate(Min("product_price"), Max("product_price"))

    return {
        'categories' : categories,
        'sub_categories' : sub_categories,
        'vendors' : vendors,
        'address' : address,
        'min_max_price' : min_max_price
    }