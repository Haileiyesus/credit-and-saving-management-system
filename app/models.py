from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class data(models.Model):
    email = models.EmailField(
        max_length=30,
    )
    username = models.CharField(
        max_length=30,
    )
    password = models.CharField(
        max_length=30,
    )
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

class act(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN2 = "ADMIN2", "Admin2"
        FINANCE = "FINANCE", "Finance"
        STAFF = "STAFF", "Staff"

    role = models.CharField(max_length=50, choices=Role.choices)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.role = self.Role.ADMIN
    #     return super().save(*args, **kwargs)

class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=act.Role.CUSTOMER)

class Customer(act):
    objects = CustomerManager()
    
    class Meta:
        proxy = True

class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=act.Role.ADMIN)

class Admin(act):
    objects = AdminManager()

    class Meta:
        proxy = True

class Admin2Manager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=act.Role.ADMIN2)

class Admin2(act):
    objects = Admin2Manager()

    class Meta:
        proxy = True

class FinanceManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=act.Role.FINANCE)

class Finance(act):
    objects = FinanceManager()

    class Meta:
        proxy = True

class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=act.Role.STAFF)

class Staff(act):
    objects = StaffManager()

    class Meta:
        proxy = True

User = get_user_model()

class AdminProfile(models.Model):
    user = models.OneToOneField(Admin, on_delete=models.CASCADE)
    admin_id = models.IntegerField(null=True, blank=True)
    balance1=models.IntegerField(default=0)

class CustomerProfile(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='profile') ##### probem with duplication#######
    customer_id = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=100,default='')
    address= models.CharField(max_length=100,default='')
    sex= models.CharField(max_length=100,default='')
    age= models.IntegerField(default=0)
    phone_no= models.CharField(max_length=100,default='')
    salary = models.PositiveIntegerField(default=0)
    salary_p = models.PositiveIntegerField(default=10)
    balance = models.PositiveIntegerField(default=0)
    willing_total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username

class Admin2Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin2_id = models.IntegerField(null=True, blank=True)

class FinanceProfile(models.Model):
    user = models.ForeignKey(Finance, on_delete=models.CASCADE)
    finance_id = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    
    
    
class StaffProfile(models.Model):
    user = models.ForeignKey(Staff, on_delete=models.CASCADE,related_name='profile1')
    staff_id = models.IntegerField(null=True, blank=True)
    address= models.CharField(max_length=100,default='')
    sex= models.CharField(max_length=100,default='')
    age= models.IntegerField(default=0)
    phone_no= models.CharField(max_length=100,default='')
    level= models.CharField(max_length=100,default='') 
    
    def __str__(self):
        return self.user.username   

    

# Create profiles when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == act.Role.ADMIN:
        AdminProfile.objects.create(user=instance)
    elif created and instance.role == act.Role.CUSTOMER:
        CustomerProfile.objects.create(user=instance)
    elif created and instance.role == act.Role.ADMIN2:
        Admin2Profile.objects.create(user=instance)
    elif created and instance.role == act.Role.FINANCE:
        FinanceProfile.objects.create(user=instance)
    elif created and instance.role == act.Role.STAFF:
        StaffProfile.objects.create(user=instance)


    # class Userprofile(models.Model):
    #     user=models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    #     bio=models.text_field(blank=True)


# class Staffs(models.Model):
#     admin = models.OneToOneField(Staff, on_delete = models.CASCADE)
#     address = models.TextField()
#     sex = models.TextField()
#     age = models.TextField()
#     phone_no = models.TextField()
#     level = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    



class Dilla_emp(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField( max_length=30,)
    Salary = models.PositiveIntegerField(default=0)
    # Salary_10 = models.PositiveIntegerField(default=0)
    Department = models.CharField(max_length=30)
    # Total=  models.PositiveIntegerField(default=0) for the total_salary_10
    account_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.firstname

    
################### staff leave #####################
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
################### cust leave #####################

class LeaveReportCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomerProfile , on_delete=models.CASCADE,null=True)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    cus_id = models.IntegerField(null=True, blank=True)
    objects = models.Manager()
    
    ############# cust Feedback############
class ComplainCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE,null=True,related_name='complaints')
    complain = models.TextField()
    complain_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
############loan##############

class LoanRequest(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE,null =True)
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reject_reason = models.TextField(blank=True)
    loan_amount = models.IntegerField(default=0)
    cust_id = models.IntegerField(null=True, blank=True)
    date=models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    
    

class Account(models.Model):
    user= models.ForeignKey(Customer, on_delete=models.CASCADE,null =True)
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE,null =True)
    account_no=models.CharField(max_length=100,default='')
    account_balance=models.PositiveIntegerField(default=0)
    account_pass=models.CharField(max_length=100,default='')
    cust_id = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.user.username
    
class CustBalance(models.Model):
    customer_id = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE,null =True)
    salary_10 = models.IntegerField(default=0)
    willing = models.PositiveIntegerField(default=0)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    
