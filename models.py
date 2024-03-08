from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.db.models import Sum


# Create your models here.




class CustomUser(AbstractUser):
    user_type_choices = ((1, "Admin"), (2, "Staff"), (3, "Merchant"), (4, "Customer"))
    user_type = models.CharField(max_length=255, choices=user_type_choices, default=1)

    class Meta:
        db_table = 'customuser'


class AdminUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'adminuser'


class MerchantUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    company_name = models.CharField(max_length=255)
    gst_details = models.CharField(max_length=255)
    address = models.TextField()
    is_added_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'merchantuser'


class CustomerUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customeruser'
      


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'categories'

    def get_absolute_url(self):
        return reverse("category_list")

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'subcategories'

    def get_absolute_url(self):
        return reverse("sub_category_list")


class ProductVerificationNotification(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'productverificationnotification'


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    is_verified = models.BooleanField(default=False)
    url_slug = models.CharField(max_length=255)
    subcategories_id = models.ForeignKey(SubCategories, on_delete=models.CASCADE)
    protein_content = models.CharField(max_length=255, null=True, blank=True)
    fat_content = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_max_price = models.CharField(max_length=255)
    product_discount_price = models.CharField(max_length=255)
    product_description = models.TextField()
    product_long_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by_merchant = models.ForeignKey(MerchantUser, on_delete=models.CASCADE)
    in_stock_total = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'products'
        

class UnverifiedProducts(Products):

    class Meta:
        proxy = True
        verbose_name = 'Unverified Product'
        verbose_name_plural = 'Unverified Products'

        db_table = 'unverifiedproducts'


class ProductMedia(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    media_type_choice = ((1, "Image"), (2, "Video"))
    media_type = models.CharField(max_length=255)
    media_content = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'productmedia'


class ProductTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type_choices = ((1, "BUY"), (2, "SELL"))
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    transaction_product_count = models.IntegerField(default=1)
    transaction_type = models.CharField(choices=transaction_type_choices, max_length=255)
    transaction_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'producttransaction'


class ProductDetails(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    title_details = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)
    class Meta:
        db_table = 'productdetails'


class ProductAbout(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'productabout'


class ProductTags(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'producttags'



class ProductReviews(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    review_image = models.FileField()
    rating = models.CharField(default="5", max_length=255)
    review = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'productreviews'

class ProductReviewVoting(models.Model):
    id = models.AutoField(primary_key=True)
    product_review_id = models.ForeignKey(ProductReviews, on_delete=models.CASCADE)
    user_id_voting = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        db_table = 'productreviewvoting'


class ProductVarient(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productvarient'


class ProductVarientItems(models.Model):
    id = models.AutoField(primary_key=True)
    product_varient_id = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productvarientitems'


from django.db.models import Sum

class CustomerOrders(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_code = models.CharField(max_length=255)
    discount_amt = models.DecimalField(max_digits=10, decimal_places=2)
    product_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customerorders'

    @staticmethod
    def get_sales_data():
        sales_data = CustomerOrders.objects.values('product_id__added_by_merchant__company_name') \
            .annotate(total_sales=Sum('purchase_price')) \
            .order_by('product_id__added_by_merchant__company_name')
        return sales_data




class OrderDeliveryStatus(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(CustomerOrders, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    status_message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orderdeliverystatus'


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminUser.objects.create(auth_user_id=instance)

        if instance.user_type == 2:
            MerchantUser.objects.create(auth_user_id=instance, company_name="", gst_details="", address="")
        if instance.user_type == 3:
            CustomerUser.objects.create(auth_user_id=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminuser.save()

    if instance.user_type == 2:
        instance.merchantuser.save()
    if instance.user_type == 3:
        instance.customeruser.save()
