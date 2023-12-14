from django.shortcuts import render
from . models import User
from django.contrib.auth.hashers import make_password, check_password
import requests
import random	
def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def blog(request):
	return render(request, 'blog.html')

def shopping_cart(request):
	return render(request, 'shoping-cart.html')

def contact(request):
	return render(request, 'contact.html')

def product(request):
	return render(request, 'product.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg = "Email already registered"
			return render(request, 'signup.html', {'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=make_password(request.POST['password']),
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
			encrpassword=make_password(request.POST['password'])
			checkpassword=check_password(request.POST['password'], user.password)
			if checkpassword==True:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_picture']=user.profile_picture.url
				return render(request, 'index.html')
			else:
				msg="Password is incorrect"
				return render(request, 'login.html',{'msg':msg})
		except:
			return render(request, 'login.html', {'msg':'Email is incorrect'})
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
			return render(request, 'otp.html', )
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
			return render(request, 'profile.html', {'user':user}, {'msg':msg})
	else:

		return render(request, 'profile.html', {'user':user})

