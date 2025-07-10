from django.utils import timezone
from django.db.models import Avg
from django.db import models



class User(models.Model):
    username=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(unique=True,blank=True,null=True)
    password=models.CharField(max_length=25,blank=True,null=True)
    profile_picture = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    otp=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.name
    

class Sub_category(models.Model):
    scategory=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.name
    

class Price(models.Model):
    name=models.CharField(max_length=90,blank=True,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    maincategory=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    subcategory=models.ForeignKey(Sub_category,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=90,blank=True,null=True)
    price=models.IntegerField()
    del_price=models.IntegerField()
    image=models.ImageField(upload_to="ststic",blank=True,null=True)
    des=models.TextField()


    average_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, default=0.0) 

    def update_average_rating(self):
        avg_rating = self.reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        self.average_rating = round(avg_rating * 2) / 2  # Round to nearest 0.5
        self.save()


    def __str__(self):
        return self.name
    

class Add_to_cart(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=90,blank=True,null=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to="media",blank=True,null=True)
    quantity=models.IntegerField(blank=True,null=True)
    total_price=models.IntegerField()

    def __str__(self):
        return self.name
    



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code




class Wishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=90, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="media", blank=True, null=True)

    class Meta:
        unique_together = ('user_id', 'product_id') # A user can add a product to wishlist only once

    def __str__(self):
        return f"{self.user_id.username}'s Wishlist: {self.name}"





class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(default=timezone.now) # Use timezone.now

    def __str__(self):
        return f"Order #{self.id} by {self.first_name} {self.last_name}"






class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.name} in Order #{self.order.id}"
    




class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    # Add this new field to store the name provided in the review form
    reviewer_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
        
    def __str__(self):
        # Use reviewer_name if available, otherwise fallback to username
        display_name = self.reviewer_name if self.reviewer_name else self.user.username
        return f"Review by {display_name} for {self.product.name} with rating {self.rating}"




class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - Subject: {self.subject}"