from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
import django.utils.timezone

# Choices
RATING = (
    (1, '⭐☆☆☆☆'),
    (2, '⭐⭐☆☆☆'),
    (3, '⭐⭐⭐☆☆'),
    (4, '⭐⭐⭐⭐☆'),
    (5, '⭐⭐⭐⭐⭐'),
)

# Status Choices
STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')
)

class Users(AbstractUser):
    User_Type = (
        (1,'Admin'),
        (2,'Users')
    )
    user_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345', primary_key=True)
    profile_pic = models.ImageField(upload_to='media/profile_pic',null=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    gender = models.CharField(max_length=20,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    no_street_line = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=20,null=True, blank=True, default='Ahmedabad')
    pincode = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=20,null=True, blank=True, default='Gujarat')
    country = models.CharField(max_length=20,null=True, blank=True, default='India')
    user_type = models.IntegerField(choices=User_Type,default=2)
    otp = models.IntegerField(null=True, blank=True)
    vendor_id = models.CharField(max_length=30,null=True, blank=True)

class Category(models.Model):
    category_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet='abcdefgh12345', primary_key=True)
    category_name = models.CharField(max_length=30, unique=True, null=False)
    category_img = models.ImageField(upload_to='media/category_img',null=True)
    date = models.DateTimeField(default=django.utils.timezone.now)

class Sub_Category(models.Model):
    subcategory_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='subcat', alphabet='abcdefgh12345', primary_key=True)
    subcategory_name = models.CharField(max_length=30, unique=True, null=False)
    subcategory_img = models.ImageField(upload_to='media/subcategory_img', null=True)
    date = models.DateTimeField(default=django.utils.timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='sub_categories')

class Tags(models.Model):
    pass

class Vendor_Account_Request(models.Model):
    Account_Request_Status = (
        (1,'Request Pending'),
        (2,'Request Approve'),
        (3,'Request Reject'),
    )
    vendor_account_request_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet='abcdefgh12345', primary_key=True)
    vendor_account_status = models.IntegerField(choices=Account_Request_Status,default=1)
    date = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

class Vendor(models.Model):
    vendor_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet='abcdefgh12345', primary_key=True)
    vendor_name = models.CharField(max_length=100, null=True, blank=True)
    vendor_img = models.ImageField(upload_to='media/vendor_img', null=True)
    vendor_cover_img = models.ImageField(upload_to='media/vendor_img', null=True)
    vendor_description = models.TextField(null=True, blank=True)
    vendor_address = models.CharField(max_length=150, null=True, blank=True)
    vendor_phone = models.CharField(max_length=20, null=True, blank=True)
    shipping_on_time = models.CharField(max_length=20, null=True, blank=True)
    vendor_rating = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(default=django.utils.timezone.now)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

class Product(models.Model):
    product_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='pro', alphabet='abcdefgh12345', primary_key=True)
    product_name = models.CharField(max_length=100, null=False)
    product_img = models.ImageField(upload_to='media/product_img', null=True)
    product_description = models.TextField(null=True, blank=True)
    product_ingredients = models.TextField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_old_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField(null=False)
    date = models.DateTimeField(default=django.utils.timezone.now)
    product_status = models.BooleanField(default=True)
    product_in_stock = models.BooleanField(default=True)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True, related_name="sub_category")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, related_name="vendor")
    tags = models.CharField(max_length=100, null=True, blank=True)

    def get_precentage(self):
        new_price = (self.product_price / self.product_old_price) * 100
        return new_price

    def get_save(self):
        save_price = (self.product_old_price - self.product_price)
        return save_price

class Product_Images(models.Model):
    product_images_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='img', alphabet='abcdefgh12345', primary_key=True)
    product_images = models.ImageField(upload_to='media/product_img', null=True)
    date = models.DateTimeField(default=django.utils.timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="p_images")

class Product_Review(models.Model):
    product_review_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='rev', alphabet='abcdefgh12345', primary_key=True)
    product_review_message = models.TextField(null=True, blank=True)
    product_rating = models.IntegerField(choices=RATING, default=None)
    product_review_date = models.DateTimeField(default=django.utils.timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="reviews")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, related_name="user")

    def get_rating(self):
        return self.product_rating
        
class Wishlist(models.Model):
    wishlist_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345', primary_key=True)
    wishlist_date = models.DateTimeField(default=django.utils.timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

class Address(models.Model):
    address_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345', primary_key=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

# class Cart(models.Model):
#     cart_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345', primary_key=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
#     product_quantity = models.IntegerField(null=True)
#     system_id = models.CharField(max_length=100, null=True)

class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=30, default="cod")
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    invoice_no = models.CharField(max_length=20)
    product_status = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    item_id = models.CharField(max_length=20, null=True)
    qty = models.IntegerField(default=0)
    price =  models.DecimalField(max_digits=10, decimal_places=2)
    total =  models.DecimalField(max_digits=10, decimal_places=2)
