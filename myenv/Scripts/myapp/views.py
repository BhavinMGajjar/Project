from django.shortcuts import render
#from django.contrib.auth.hashers import make_password, check_password
from . models import User, Product, Wishlist
from django.shortcuts import redirect
import requests
import random	

def index(request):
	return render(request, 'index.html')

def seller_index(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=="Buyer":
		return render(request, 'index.html')
	else:
		return render(request, 'seller-index.html')

def about(request):
	return render(request, 'about.html')

def blog(request):
	return render(request, 'blog.html')

def shopping_cart(request):
	return render(request, 'shoping-cart.html')

def contact(request):
	return render(request, 'contact.html')

def product(request, cat):
	products=Product()
	if cat=="all":
		products=Product.objects.all()
	elif cat=="Women":
		products=Product.objects.filter(product_category="Women")
	elif cat=="Men":
		products=Product.objects.filter(product_category="Men")
	elif cat=="Kids":
		products=Product.objects.filter(product_category="Kids")
	return render(request, 'product.html', {'products':products})

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg = "Email already registered"
			return render(request, 'signup.html', {'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					usertype=request.POST['usertype'],
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					#password=make_password(request.POST['password']),
					profile_picture=request.FILES['profile_picture']

				)
				msg = "User Signed up Successfully"
				return render(request, 'signup.html', {'msg':msg})
			else:
				msg="Password and Confirm Password not matched"
				return render(request, 'signup.html', {'msg':msg})


	else:
		return render(request, 'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=="Buyer":
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_picture']=user.profile_picture.url
					wishlists=Wishlist.objects.filter(user=user)
					request.session['wishlist_count']=len(wishlists)
					return render(request, 'index.html')
				else:
				
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_picture']=user.profile_picture.url
					return render(request, 'seller-index.html')
			else:
				msg="Password is incorrect"
				return render(request, 'login.html',{'msg':msg})
		except:
			msg="Email incorrect"
			return render(request, 'login.html', {'msg': msg})
	else:
		return render(request, 'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_picture']
		return render(request, 'login.html')
	except:
		return	render(request, 'login.html')


def forgot_password(request):
	if request.method=='POST':
		try:
			otp=random.randint(1000,9999)
			user=User.objects.get(mobile=request.POST['mobile'])
			mobile=request.POST['mobile']
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"LjilSdTOgPD1Qon2REw6fXJvpBexCGF5raHYVM3NsZyUb78WKuRXkKr418N65UyIxwuVZzJf7tW23hcb","variables_values":str(otp),"route":"otp","numbers":mobile}
			headers = { 'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			request.session['mobile']=mobile
			request.session['otp']=otp
			return render(request, 'otp.html')
		except:
			msg="Mobile number does not exist"
			return render(request, 'forgot-password.html', {'msg':msg})
	else:
		return render(request, 'forgot-password.html')


def verify_otp(request):
	otp=request.session['otp']
	uotp=request.POST['utop']

	if otp==utop:
		del request.session['otp']
		return render(request, 'new-password.html')
	else:
		msg="Invalid OTP"
		return render(request, 'otp.htmnl', {'msg':msg})

def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		email=request.session['email']
		user=User.objects.get(email=email)
		user.password=request.POST['new_password']
		user.save()
		return redirect('logout')
	else:
		msg="New & Confirm Password not matched"
		return render(request, 'new-password.html', {'msg':msg})

def profile(request):

	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
			user.save()
			request.session['profile_picture']=user.profile_picture.url
			msg="Profile updated Successfully"
			if user.usertype=="Buyer":
				return render(request, 'profile.html', {'user':user,'msg':msg})
			else:
				return render(request, 'seller-profile.html', {'user':user,'msg':msg})
				
	else:
		if user.usertype=="Buyer":
			return render(request, 'profile.html', {'user':user})
		else:
			return render(request, 'seller-profile.html', {'user':user})
def change_password(request):
	email=request.session['email']
	user=User.objects.get(email=email)
	if request.method=="POST":		
		checkpassword=check_password(request.POST['old_password'], user.password)
		if checkpassword==True:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=make_password(request.POST['new_password'])
				user.save()
				return redirect('logout')
			else:
				msg="New & Cofirm passwords not matched"
				return render(request, 'change-password.html',{'msg':msg})
		else:
			msg="Invalid Old Password"
			return render(request, 'change-password.html',{'msg':msg})
	else:
		if user.usertype=="Buyer":
			return render(request, 'change-password.html')
		else:
			return render(request, 'seller-change-password.html')


def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
					seller = seller,
					product_category=request.POST['product_category'],
					product_brand=request.POST['product_brand'],
					product_size=request.POST['product_size'],
					product_price=request.POST['product_price'],
					product_name=request.POST['product_name'],
					product_desc=request.POST['product_desc'],
					product_image=request.FILES['product_image'],
			)
		msg="Product added Successfully"
		return render(request, 'seller-add-product.html', {'msg':msg})
	else:
		return render(request, 'seller-add-product.html')


def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])
	products=Product.objects.filter(seller=seller)
	return render(request, 'seller-view-product.html', {'products': products})

def seller_product_detail(request, pk):
	product=Product.objects.get(pk=pk)
	return render(request, 'seller-product-detail.html', {'product':product})

def seller_product_edit(request, pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_category=request.POST['product_category']
		product.product_brand=request.POST['product_brand']
		product.product_size=request.POST['product_size']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
			product.save()
			msg="Product Edited Successfully"
			return render(request, 'seller-product-edit.html', {'product':product, 'msg':msg})

	else:
		return render(request, 'seller-product-edit.html', {'product':product})


def seller_product_delete(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('seller-view-product')

def product_details(request,pk):
	wishlist_flag=False
	user=User.objects.get(email=request.session['email'])  
	product=Product.objects.get(pk=pk)
	try:
			Wishlist.objects.get(user=user, product=product)
			wishlist_flag=True
	except:
			pass
	return render(request, 'product-details.html', {'product':product, 'wishlist_flag': wishlist_flag})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user, product=product)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request, 'wishlist.html', {'wishlists': wishlists })

def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user, product=product)
	wishlist.delete()
	return redirect('wishlist')
