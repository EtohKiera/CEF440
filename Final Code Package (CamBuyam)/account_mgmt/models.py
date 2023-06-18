from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
#from django.utils.translation import ugettext_lazy as _

# custom user manager that inherits from BaseUserManager:
# This manager provides methods for creating regular users and superusers.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,fname=None,lname=None,town=None,phone=None, **extra_fields):
        if not email:
            raise ValueError(('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.fname = fname
        user.lname = lname
        user.town = town
        user.phone = phone
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    
    class Meta:
        app_label='account_mgmt' 


# Creating a custom user model that extends the AbstractBaseUser class:
# In this model, we define the fields for our custom user, including email, name, date of birth, 
#   profile photo, and various permissions. We also specify the custom user manager we created earlier.

class CustomUser(AbstractBaseUser):
    email = models.EmailField(('Email address'), unique=True)
    fname = models.CharField(('First name'), max_length=50)  
    lname = models.CharField(('Last name'), max_length=50)
    town = models.CharField(('Town'), max_length = 20, null=False)
    joined_at = models.DateField(auto_now_add = True, null=True, blank=True)
    is_staff = models.BooleanField(('staff_status'), default = False)
    phone = models.CharField( max_length=15) 

   # date_of_birth = models.DateField(('Date of birth'), null=True, blank=True)
    profile_photo = models.ImageField(('Profile photo'), upload_to='profile_photos/',default='default-profile-pic.jpeg', null=True, blank=True)
    is_active = models.BooleanField(('Active'), default=True)
    # is_staff = models.BooleanField(('Staff status'), default=False)
    is_superuser = models.BooleanField(('Superuser status'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        app_label='account_mgmt'



class CustomAdmin(models.Model):
      admin_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, default=1)
      join_code = models.CharField( max_length=50,null=False,blank=True)  
    

class Seller(models.Model):
      seller_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, default=1)
      verification_status = models.CharField( default='unverified' ,max_length=20)
      bio = models.CharField( default='No Bio ' ,max_length=200)
      is_seller = models.BooleanField( default = True)

class AccountVerificationPhotos(models.Model):
      seller_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE, default=1)
      uploaded_at = models.DateField(auto_now_add = True, null=True, blank=True)
      IDnumber = models.CharField( default='0000000000' ,max_length=20)
      photo1 = models.ImageField(upload_to='kyc_verification_photos/', null=False, blank=False)
      photo2 = models.ImageField(upload_to='kyc_verification_photos/', null=False, blank=False)
      photo3 = models.ImageField(upload_to='kyc_verification_photos/', null=False, blank=False)
      verification_date = models.DateField(null=True, blank=True)
      verified_by =  models.ForeignKey("CustomAdmin", on_delete=models.CASCADE, null=True)
      verification_status = models.CharField( default='pending' ,max_length=20)


