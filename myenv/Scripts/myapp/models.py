from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.BigIntegerField()
	address=models.TextField(max_length=100)
	password=models.CharField(max_length=100)
	profile_picture=models.ImageField(default="", upload_to="profile_picture")
	usertype=models.CharField(max_length=100, default="buyer")

def __str__(self):
	return self.fname

class Product(models.Model):

	category=(

			("Men","Men"),
			("Women","Women"),
			("Kids","Kids"),
			)

	brand=(

			("Lewis","Lewis"),
			("FCUK","FCUK"),
			("Pepe","Pepe"),
		)

	size=(
			("Small","Small"),
			("M","M"),
			("L","L"),
			("XL","XL"),

		)
	
	seller=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	product_name=models.CharField(max_length=100, blank=True, null=True)
	product_price=models.PositiveIntegerField(blank=True, null=True)
	product_category=models.CharField(max_length=100,choices=category, blank=True, null=True )
	product_brand=models.CharField(max_length=100,choices=brand, blank=True, null=True)
	product_size=models.CharField(max_length=100,choices=size, blank=True, null=True)
	product_image=models.ImageField(upload_to="product_images/", blank=True, null=True)
	product_desc=models.TextField(blank=True, null=True)

	def __str__(self):
		return self.seller.fname+ "-"+self.product_name

class Wishlist(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	product=models.ForeignKey(Product, on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.fname+" - "+self.product.product_name