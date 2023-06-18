from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import *
from product_mgmt.models import *


#CBV for login
class CustomLoginView(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('home')

#CBV for logout
class CustomLogOutView(LogoutView):
    next_page = 'home'

def home(request):
    user = request.user
    todays_picks = Product.objects.all()
    return render(request, 'home2.html', {'user':user,'todays_picks':todays_picks})

def seller_registration(request):
    if request.method == 'POST':
      
     # person = Registration(email=email, fname=fname, lname=lname,town=town, phone=phone, )
       user = CustomUser.objects.create_user( request.POST['email'],
                                              request.POST['password1'], 
                                              request.POST['fname'], 
                                              request.POST['lname'], 
                                              request.POST['town'], 
                                              request.POST['phone'],)
       seller = Seller(seller_id=user)
       seller.save() 
       return redirect ('login') 
    else:  
       return render(request, 'register.html')




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect(reverse('profile',args=[user.id]))
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})

def seller_profile(request,user_id):
    user = request.user
    seller = Seller.objects.get(seller_id = user_id)
    dic = {'user':user,
           'seller': seller,
           'products': Product.objects.filter(seller_id = seller),
           'user_is_owner': (seller.seller_id==user),
           'total_stores' : Store.objects.filter(seller=seller).count()
          }
    if seller is None:
        return redirect('home')
    return render(request,'seller_profile.html', dic)    

#UPDATE PROFILE PIC
def change_profile_photo(request):
    if request.method=='POST':
        pic = request.FILES.get('pic')
        user=CustomUser.objects.get(email=request.user.email)
        user.profile_photo =pic
        user.save()
        return redirect(reverse('profile',args=[user.id]))  
    return render(request, 'changeProfilePicture.html')

  
#Edit Biography
def edit_bio(request):
    user= CustomUser.objects.get(email=request.user.email)
    seller = Seller.objects.get(seller_id = user.id)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        seller.bio = bio
        seller.save()
        return redirect(reverse('profile',args=[user.id]))
    else:
        return render(request, 'edit-bio.html')

#Seller Verify account by submitting KYC info
def verify_account(request):
    user= CustomUser.objects.get(email=request.user.email)
    seller = Seller.objects.get(seller_id = user.id)

    if request.method == 'POST':
        idnumber = request.POST.get('IDnumber')
        photo1 = request.FILES.get('front-photo')
        photo2 = request.FILES.get('back-photo')
        photo3 = request.FILES.get('selfie-photo')   
        kyc_info= AccountVerificationPhotos(seller_id=user,IDnumber=idnumber, photo1=photo1, photo2=photo2, photo3=photo3) 
        kyc_info.save()
        seller.verification_status="Pending"
        seller.save()
        return redirect(reverse('profile',args=[user.id]))
    else:
        return render(request, 'submitKYC.html')

#ADMIN ACCOUNTS
def admin_registration(request):
    if request.method == 'POST':
      if request.POST.get('join-code')== "abc12345":
            error_message = ""
            # person = Registration(email=email, fname=fname, lname=lname,town=town, phone=phone, )
            user = CustomUser.objects.create_user( request.POST['email'],
                                                    request.POST['password1'], 
                                                    request.POST['fname'], 
                                                    request.POST['lname'],
                                                    "buea",  
                                                    request.POST['phone'],
                                                    is_staff = True)
            admin = CustomAdmin(admin_id=user, join_code= request.POST.get('join-code'))
            admin.save() 
            return redirect ('admin-login') 
      else:
          error_message="Invalid Join Code"
    else:
        error_message= ""
          
    return render(request, 'adminSignup.html',{'error_message':error_message})



def admin_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin-dashboard')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = ''
    return render(request, 'adminLogin.html', {'error_message': error_message})


def admin_dashboard(request):
    user = request.user
    admin = CustomAdmin.objects.get(admin_id = user.id)
    all_pending = AccountVerificationPhotos.objects.filter(verification_status='pending')

    dic = {'user':user,
            'total_pending_kyc':all_pending.count,

            }
    if user.is_authenticated and user.is_staff:
          return render(request,'adminDashboard.html', dic)  


def pending_kyc_verification(request):
    user=request.user
    if user.is_authenticated and user.is_staff:
      all_pending = AccountVerificationPhotos.objects.filter(verification_status='pending')
      users = CustomUser.objects.all()
      return render(request,'pending_kyc.html', {'all_pending':all_pending,'users':users})  
    else:
        return redirect('home')


def verify_seller(request,user_id):
    admin=request.user
    if admin.is_authenticated and admin.is_staff:
      kyc_info = AccountVerificationPhotos.objects.get(seller_id=user_id )
      user = CustomUser.objects.get(id = user_id)
      return render(request,'verifySeller.html', {'kyc_info':kyc_info,'user':user})  
    else:
        return redirect('home')        
def approve_seller(request,user_id):
    admin=request.user
    if admin.is_authenticated and admin.is_staff:
      kyc_info = AccountVerificationPhotos.objects.get(seller_id=user_id )
      kyc_info.verification_status= "approved"
      kyc_info.verified_by=CustomAdmin.objects.get(admin_id = request.user.id)
      kyc_info.save()
      seller = Seller.objects.get(seller_id = user_id)
      seller.verification_status="Verified"
      seller.save()
      return redirect('pending-kyc') 
    else:
      return redirect('home')  

def decline_seller(request,user_id):
    admin=request.user
    if admin.is_authenticated and admin.is_staff:
      kyc_info = AccountVerificationPhotos.objects.get(seller_id=user_id )
      kyc_info.verification_status= "declined"
      kyc_info.verified_by=CustomAdmin.objects.get(admin_id = request.user.id)
      kyc_info.save()
      seller = Seller.objects.get(seller_id = user_id)
      seller.verification_status="declined"
      seller.save()
      return redirect('pending-kyc') 
    else:
      return redirect('home')  
