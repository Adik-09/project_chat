from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from django.core.mail import send_mail

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home-page')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login-page')

    return render(request, 'login.html')
    
def register(request):
   if request.method=='POST':
      username=request.POST.get('username')
      email=request.POST.get('email')
      password=request.POST.get('password')

      user=User.objects.filter(username=username).first()    # ensure only one username exist.
      if user:
         messages.error(request,"Username already exist..")
         return redirect('register-page')
      else:
         messages.success(request,"Username created successsful..")
         user=User.objects.create_user(username=username,email=email,password=password)  # add data and [hashed password] to user table.
         return redirect('login-page')
   
   return render(request,'register.html')

def forget_pass(request):
   if request.method=='POST':
      user_name=request.POST.get('username')
      user_email=request.POST.get('email')

      if User.objects.filter(username=user_name,email=user_email).exists():
         user_otp = str(random.randint(100000, 999999))
         subject = "Your OTP Code"
         message = f"Your OTP is {user_otp}. It is valid for 5 minutes."
         send_mail(subject, message, "aditya.kasture09@gmail.com",[user_email])
         request.session["otp_user"]=user_otp
         request.session["user_name"]=user_name
         request.session["user_email"]=user_email
         request.session.set_expiry(30)
         return redirect('verify-otp')
      else:
         messages.error(request,"Email or username do not exist")
      
   return render(request,'forget_pass.html')  

def verify_otp(request):
   if request.method=="POST":
      entered_otp=request.POST.get('otp')
      user_otp = request.session.get('otp_user')

      if entered_otp==user_otp:
         del request.session['otp_user']
         request.session['otp_verified'] = True
         return redirect('change-password')
      else:
         messages.error(request,"Invalid otp or time out")
         
   return render(request,'verify_otp.html')

def change_password(request):
    if not request.session.get("otp_verified"):
        messages.error(request, "OTP verification required!")
        return redirect("forget-page")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match! Please try again.")
            return redirect('change-password')

        user_name = request.session.get('user_name')
        user_email = request.session.get('user_email')

        if not user_name or not user_email:
            messages.error(request, "Time out or invalid data! Please try again.")
            return redirect('forget-page')

        try:
            user = User.objects.get(username=user_name, email=user_email)
            user.set_password(new_password)  # Securely update the password
            user.save()

            request.session.flush()  # Clear session after password reset
            messages.success(request, "Password changed successfully! Please log in with your new password.")
            return redirect('login-page')
        except User.DoesNotExist:
            messages.error(request, "User not found! Please try again.")
            return redirect('forget-page')

    return render(request, "change_password.html")


@login_required
def user_logout(request):
   logout(request)
   messages.success(request, "Logout successfull !.. ")
   return redirect('login-page')