from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import data,act,Customer,CustomerProfile,StaffProfile,Dilla_emp,Staff,LeaveReportStaff,ComplainCustomer,LeaveReportCustomer,LoanRequest,AdminProfile, FinanceProfile,CustBalance,Account
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Sum
from django.http import Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models.functions import ExtractMonth
from django.contrib.auth.hashers import make_password


    # Rest of your code...

# @login_required(login_url="login")
def HomePage(request):
    print(request.user.id,"Welcome  ")
    return render (request,'admin_home.html')

def about_page(request):
    return render(request,'about.html')

def contact_us(request):
    return render(request,'contact_us.html')

def FrontPage(request):
    return render(request, "front.html")

# #FOR CUSTOMER ##
def SignupPage(request):
    if request.method == "POST":
        email = request.POST["email"]
        uname = request.POST["username"]
        pass1 = request.POST["password1"]
        first = request.POST["firstname"]
        last = request.POST["lastname"]
        dept = request.POST["department"]
        sal = request.POST["salary"] 
        address = request.POST["address"]
        sex = request.POST["sex"]
        age = request.POST["age"]
        phone_no = request.POST["phone_no"]
        salary_p = request.POST["salary_p"]
        account=request.POST["account"]
        
        

        # Check if required fields are filled
        if not email or not uname or not pass1 or not first or not last or not dept or not sal or not address or not sex or not age or not phone_no or not salary_p  or not account:
            messages.error(request, "Please fill all required fields.")
            return redirect("signup")

        # Check if passwords match
        if pass1 != request.POST["password2"]:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")
        
        if int(salary_p) < 10 and int(salary_p) > 100:
            messages.error(request, "Salary_10 should be greater than 10 percent and lessthan 100 percent.")
            return redirect("signup") 
        if len(account) < 5 or len(account)> 13:
            messages.error(request, "Account is invalid.")
            return redirect("signup") 

        # Check if the user exists in Dilla_emp database
        try:
            employee = Dilla_emp.objects.get(email=email, firstname=first, lastname=last, Department=dept, Salary=sal,account_number=account)
        except Dilla_emp.DoesNotExist:
            messages.error(request, "User does not exist in Dilla_emp database.")
            return redirect("signup")

        user = act.objects.create_user(
            username=uname,
            email=email,
            password=pass1,
            first_name=first,
            last_name=last,
            role=act.Role.CUSTOMER
        )

        profile = CustomerProfile.objects.create(
            user=user,
            customer_id=employee.id,
            department=dept,
            salary=sal,
            address=address,
            phone_no=phone_no,
            sex=sex,
            age=age,
            salary_p=salary_p
        )
        
        acc=Account.objects.create(
            user=user,
            customer_id=profile,
            account_no=account,
            cust_id=profile.customer_id,
        )
        cus = CustomerProfile.objects.filter(customer_id=None)
        if cus.exists():
            cus.delete()
        return redirect("login")
    return render(request, "signup.html")

@csrf_exempt
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            if user.role == "ADMIN":
                return redirect('admin_home')
            elif user.role == "CUSTOMER":
                customer_profile = CustomerProfile.objects.get(user=user)
                return redirect('cust_home',customer_id=customer_profile.customer_id)
            elif user.role == "ADMIN2":
                return redirect('admin2_home')
            elif user.role == "FINANCE":
                return redirect('finance_home')
            elif user.role == "STAFF":
                return redirect('staff_home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='login')
def cust_home(request,customer_id):
    print(request.user.id)
    try:
        customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
        cust = CustBalance.objects.filter(customer_id=customer_profile).count()
        # loan_r=LoanRequest.objects.all()
        print("Customer")
    except CustomerProfile.DoesNotExist:
        raise Http404("CustomerProfile does not exist")

    context = {
        'customer_profile': customer_profile,
        'cust' : cust,
        # 'loan_r':loan_r,
               }
    return render(request, 'cust_home.html', context)

def LogoutPage(request):
    logout(request)
    return redirect("login")

def admin2_home(request):
    return render(request, "admin2_home.html")

def finance_home(request):
    time = datetime.now()
    try:
        finance = FinanceProfile.objects.all()
        for f in finance:
            
            if f.status == True :
                break
            if ((time.day > 3)) :
                
                f.status = True
                f.save()
    except:
        messages.error(request, "finance_home.html")
    return render(request, "finance_home.html")

def staff_home(request):
    return render(request, "staff_home.html")

################STAFF######################
def add_staff(request):
    return render(request,'add_staff.html')
def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        phone_no = request.POST.get('phone_no')
        level = request.POST.get('level')
        
        if not email or not username or not password or not first_name or not last_name or not address or not sex or not age or not phone_no or not level:
             context = {
                
                'message': 'Please fill all the required fields.',
                'message_type': 'error',
            }
             return render(request,"add_staff.html",context)

        
        try:
            user = act.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name,role=act.Role.STAFF)
            user.save()
            profile1 = StaffProfile.objects.create(
            user=user,
            staff_id=user.id,
            address=address,
            sex=sex,
            age=age,
            phone_no=phone_no,
            level=level
        )
            profile1.save()
            cus = StaffProfile.objects.filter(staff_id=None)
            if cus.exists():
                cus.delete()
            #user.save()
            # print(phone_no )
            context = {
                
                'message': 'Staff Added Successfully.',
                'message_type': 'success'
            }
            return render(request, "add_staff.html", context)

        except:
            # Add error message to the context
            context = {
                
                'message': 'Failed to Add Staff.',
                'message_type': 'error'
            }
            return render(request, "add_staff.html", context)   
def manage_staff(request):
    staf=StaffProfile.objects.all()
    staffs = Staff.objects.all()
    context = {
        "staffs": staffs,'staf':staf
}
    return render(request, "manage_staff.html", context)

# def search_staff(request):
#     search = request.POST.get('staff_search')
#     try:
#         staff_id = Staffs.objects.get(admin=search) 
#         context = {
#             "staff_id": staff_id
#             }
#         return render(request, "search_staff.html", context)
#     except:
#             messages.error(request, "No Data.")
#             return redirect('/manage_staff/')

def edit_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    staff1=StaffProfile.objects.get(staff_id=staff_id)
    
    context = {
        "staff": staff,
        "staff_id": staff_id,
        'staff1': staff1
       
    }
    return render(request, "edit_staff.html", context)

def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        phone_no = request.POST.get('phone_no')
        level = request.POST.get('level')

        try:
            # INSERTING into Customuser Model
            user = Staff.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            customer_profile=StaffProfile.objects.get(staff_id=staff_id)
            customer_profile.address=address
            customer_profile.sex=sex
            customer_profile.age=age
            customer_profile.phone_no=phone_no
            customer_profile.level=level
            customer_profile.save()
            
            context = {
                'staff_id': staff_id,
                'message': 'Staff Updated Successfully.',
                'message_type': 'success'
            }
            return render(request, "edit_staff.html", context)

        except:
            # Add error message to the context
            context = {
                'staff_id': staff_id,
                'message': 'Failed to Update Staff.',
                'message_type': 'error'
            }
            return render(request, "edit_staff.html", context)

def delete_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    try:
        staff.delete()
        
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')
      
# ###############################################################
def dilla_emp(request):
    dilla_data=Dilla_emp.objects.all()
    template=loader.get_template('dilla_emp.html')
    context={'dilla_data':dilla_data}
    return HttpResponse(template.render(context,request))

def update_dilla_emp(request, id):
  dilla_data = Dilla_emp.objects.get(id=id)
  template = loader.get_template('update_dilla_emp.html')
  context = {'dilla_data': dilla_data,}
  return HttpResponse(template.render(context, request))

def update_record(request, id):
    Salary = request.POST['salary']
    dilla_data = Dilla_emp.objects.get(id=id)
    customer_list1 = CustomerProfile.objects.all()
    if customer_list1.filter(customer_id=dilla_data.id).exists():
        dilla_data.Salary = Salary
        customer_list1.filter(customer_id=dilla_data.id).update(salary=Salary)
        dilla_data.save()
    else:
        dilla_data.Salary = Salary
        dilla_data.save()
    return HttpResponseRedirect(reverse('dilla_emp'))

def check_balance1(request,customer_id):
  try:
      customer_profile= CustomerProfile.objects.get(customer_id=customer_id)
      custbal = CustBalance.objects.filter(customer_id=customer_profile)
      cust = CustBalance.objects.filter(customer_id=customer_profile).count()
      loan_request=LoanRequest.objects.all()
      total_10 = 0
      total=0
      for c in custbal:
          total_10 += int(c.salary_10)
      
  except CustomerProfile.DoesNotExist:
      return HttpResponse("Customer doesnot exist with this id")
  context = {
      'customer_profile': customer_profile,
      'cust':cust,
      'loan_request':loan_request,
      'total_10': total_10}
  return render(request, 'check_balance.html', context)

def deposit_money(request, customer_id):
    try:
        customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
        acc1=Account.objects.get(customer_id=customer_profile)
        cust = CustBalance.objects.filter(customer_id=customer_profile).count()
        loan_request=LoanRequest.objects.all()
       
    except CustomerProfile.DoesNotExist:
        messages.error(request, 'Customer doesnt exist!')
        return redirect('cust_home', customer_id=customer_profile.customer_id)

    if request.method == 'POST':
        amount = request.POST.get('apple')
        
        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Invalid amount!')
            return redirect('deposit', customer_id=customer_profile.customer_id)
        if  amount <= acc1.account_balance :
            
            customer_profile.willing_total += amount
            customer_profile.balance += amount
            customer_profile.save()
            acc1.account_balance -=amount
            acc1.save()
            messages.success(request, 'Deposit successful!')
            return redirect('deposit', customer_id=customer_profile.customer_id)
        else:
            messages.error(request, 'Wrong account or Insufficient funds !')
            return redirect('deposit', customer_id=customer_profile.customer_id)
        
    context={
        'customer_id': customer_id,
        'customer_profile': customer_profile,
        'cust':cust,
        'loan_request':loan_request
    }
    return render(request, 'deposit.html',context)

def withdraw(request, customer_id):
    try:
        customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
        acc=Account.objects.get(customer_id=customer_profile)
        cust = CustBalance.objects.filter(customer_id=customer_profile).count()
        loan_request=LoanRequest.objects.all()
    except CustomerProfile.DoesNotExist:
        messages.error(request, 'Customer does not exist')
        return redirect('withdraw', customer_id=customer_profile.customer_id)

    if request.method == 'POST':
        amount = request.POST.get('apple')
        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Invalid amount!')
            return redirect('withdraw', customer_id=customer_profile.customer_id)

        if amount > customer_profile.willing_total:
            messages.error(request, 'Insufficient funds!')
            return redirect('withdraw', customer_id=customer_profile.customer_id)

        customer_profile.willing_total -= amount
        customer_profile.balance -= amount
        customer_profile.save()
        acc.account_balance+=amount
        acc.save()
        messages.success(request, 'Withdrawal successful!')
        return redirect('withdraw', customer_id=customer_profile.customer_id)
    context ={
        # 'customer_id': customer_id,
        "customer_profile":customer_profile,
        'cust':cust,
        "loan_request":loan_request
        
    }
    return render(request, 'withdraw.html',context)


# def account_view(request):
 
                  
# def account_view1(request,customer_id):
    
    
#################apply_leave###########
def staff_leave(request):
    staff_obj = Staff.objects.get(id=request.user.id)
    leave_data = LeaveReportStaff.objects.all()
    result = True
    
    for leave in leave_data:
        print(leave.staff_id,"        ")
        if leave.staff_id == (staff_obj):
            result = False
            print(result)
           
    context = {
        'result':result,
        "leave_data": leave_data
    }
    return render(request, "staff_leave.html", context)

def staff_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staff.objects.get(id=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_leave')
         
        ##############leave view##################
def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'staff_leave_view.html', context)

def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    
    leave.leave_status = 1
    leave.save()
    
    staff = leave.staff_id
    staff.username = f"deleted_{staff.username}"
    staff.password = make_password(None)  
    staff.save()
    return redirect('staff_leave_view')

def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')

########### Cust Leave ####################

def cust_leave(request,customer_id):
    customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
    cust = CustBalance.objects.filter(customer_id=customer_profile).count()
    loan_request=LoanRequest.objects.get(customer_id=customer_profile)
    leave_data = LeaveReportCustomer.objects.all()
    result = True
    if loan_request.loan_amount > 0:
        result = False
    for leave in leave_data:
        if int(leave.customer_id.customer_id) == int(customer_id):
            result = False
            print(result)
    
    context = {
        "leave_data": leave_data,
        'customer_profile':customer_profile,
        'loan_request': loan_request,
        'result':result,
        "cust":cust,
    }
    return render(request, 'cust_leave.html', context)


def cust_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        customer_id = request.POST.get('customer_id')
        customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
        try:
            leave_report = LeaveReportCustomer(customer_id=customer_profile, leave_date=leave_date, leave_message=leave_message, leave_status=0,cus_id=customer_id)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('/cust_leave/'+customer_id)
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('/cust_leave/'+customer_id)

###########Cust leave view####################
def cust_leave_view(request):
    leaves = LeaveReportCustomer.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'cust_leave_view.html', context)

def cust_leave_approve(request, leave_id):
    leave = LeaveReportCustomer.objects.get(id=leave_id)
    customer_profile = CustomerProfile.objects.get(customer_id=leave.cus_id)
    leave.leave_status = 1
    leave.save()
    admin_bal = AdminProfile.objects.all()
    for adm in admin_bal:
        adm.balance1 = adm.balance1 - customer_profile.balance
        adm.save()
    acc=Account.objects.get(cust_id=customer_profile.customer_id)
    acc.account_balance+=customer_profile.balance
    acc.save()
    cus=customer_profile.user
    cus.username = f"deleted_{cus.username}"
    cus.password = make_password(None)  
    cus.save()
    return redirect('cust_leave_view')

def cust_leave_reject(request, leave_id):
    leave = LeaveReportCustomer.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('cust_leave_view')

###########cust complain and reply####################
def cust_complain(request,customer_id):
    customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
    complain_data = ComplainCustomer.objects.filter(customer_id= customer_profile)
    cust = CustBalance.objects.filter(customer_id=customer_profile).count()
    loan_request=LoanRequest.objects.all()
    context = {
        "complain_data":complain_data,
        'customer_id':customer_id,
        'customer_profile':customer_profile,
        "cust":cust,
        'loan_request':loan_request
        }
    return render(request, 'cust_complain.html', context)

def cust_complain_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('/cust_complain/'+customer_id)
    else:
        complain = request.POST.get('complain_message')
        customer_id = request.POST.get('id')
        customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
        
        try:
            add_complain = ComplainCustomer(customer_id=customer_profile, complain=complain, complain_reply="")
            add_complain.save()
            messages.success(request, "Complain Sent.")
            return redirect('/cust_complain/'+customer_id)
        except:
            messages.error(request, "Failed to Send complain.")
            return redirect('/cust_complain/'+customer_id)

def cust_complain_message(request):
    complain = ComplainCustomer.objects.all()
    context = {
        "complain": complain
    }
    return render(request, 'cust_complain_message.html', context)

@csrf_exempt
def cust_complain_reply(request):
    customer_id = request.POST.get('id')
    complain_reply = request.POST.get('reply_message')

    try:
        complain = ComplainCustomer.objects.get(customer_id=customer_id)
        complain.complain_reply = complain_reply
        complain.save() 
        return HttpResponse("True")

    except:
        return HttpResponse("False")
############Transfer from finance to admin#########
def transfer_money(request):
    time = datetime.now()
    month = time.month - 1
    if time.month == 1:
        month = 12
    
    finance = FinanceProfile.objects.all()
    actiavter = False
    for f in finance:
        if ((time.day == 1 or time.day == 2 or time.day == 3) and (f.status == True)):
            actiavter = True
    customer_list = CustomerProfile.objects.all()
    total_salary_10 = 0
    c = CustomerProfile.objects.all().count()
    tot=[ [0 for j in range(3)] for i in range(c)]
    cu = 0
    for customer in customer_list:
        customer.salary_10 = int(customer.salary * 0.10)
        willing=int((customer.salary)*(customer.salary_p/100-0.10))
        tot[cu][1] = int(willing)+int(customer.salary_10)
        tot[cu][0] = customer.user
        tot[cu][2]=willing
        cu += 1
        total_salary_10 +=int(willing)+int(customer.salary_10)
    context = {
        'customer_list': customer_list, 
        'total_salary_10': total_salary_10,
        "tot":tot,
        'actiavter' : actiavter
        }
    return render(request, 'transfer_money.html', context)

def transfer_money_save(request):
    
    try:
        # finance = FinanceProfile.objects.all()
        # for f in finance:
        #     f.status = False
        #     f.save()
        cust_obj=CustomerProfile.objects.all()
        adm = AdminProfile.objects.all()
        salary_10 = 0
        will=0
        total = 0
        interest = 0
        for cust in cust_obj:
            salary_10 = int(cust.salary * 0.1)
            will=int(float(cust.salary)*( (float(cust.salary_p)/100)-0.10))
            total += (salary_10  +will)
            interest = cus.balance * 0.05
            cust.balance = int((salary_10 + will) + interest)
            cust.willing_total+=will
            cust.save()
            custbal=CustBalance.objects.create(customer_id=cust,salary_10=salary_10,willing=will)
            custbal.save()
            
        for a in adm:
            a.balance1 += total
            a.save()
            
        messages.success(request,"Transfer money Successfully")
        return redirect('transfer_money')
    except:
        messages.error(request,"Can't Transfer")
        return redirect('transfer_money')


def finance_info(request):
    custbal = CustBalance.objects.all()
    count = CustomerProfile.objects.all().count() 
    cust = CustomerProfile.objects.all() 
    result = [[0 for i in range(5)] for j in range(count)]
    counter = 0
    total1 = 0
    for i in cust:
        total = 0
        result[counter][0] = i.customer_id
        result[counter][1] = i.user.first_name
        result[counter][2] = i.user.last_name
        for j in custbal:
            if i.customer_id == j.customer_id.customer_id:
                result[counter][3] += (j.salary_10 + j.willing)
                result[counter][4] += 1
                total += (j.salary_10 + j.willing)
        i.balance=total
        i.save()
        total1 += total
        counter += 1
    
    
    context = {
        'result':result,
        'total':total1
        }
    return render(request,'finance_info.html', context)


def view_bal(request,customer_id):
    custs = CustBalance.objects.order_by('-created_at')
    customer_profile = CustomerProfile.objects.all().count() 
    loan_request=LoanRequest.objects.all()
    cust = CustBalance.objects.filter(customer_id=customer_profile).count()
    count = 0
    print(customer_id)
    for c in custs:
        if str(c.customer_id) == str(customer_id):
            count += 1
    result = [[0 for i in range(5)] for j in range(count)]
    count = 0
    for c in custs:
        
        if str(c.customer_id) == str(customer_id):
            result[count][0] = str(c.customer_id)
            result[count][1] = str(c.salary_10)
            result[count][2] = str(c.willing)
            result[count][3] = str(c.salary_10+ c.willing)
            result[count][4] = str(c.created_at)
            count += 1
    
    context = {
        'custs' : result,
        'count':count,
        'loan_request':loan_request,
        'cust':cust,
        'customer_profile':customer_profile
        
    }
    return render(request,'view_bal.html',context)

def loan_request_view(request):
    customer_profile = CustomerProfile.objects.all()
    leaves = LoanRequest.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'loan_staff.html', context)

def loan_request_approve(request, leave_id):
    try:
        leave = LoanRequest.objects.get(id=leave_id)
        leave.leave_status = 1
        leave.save()
    except:
        messages.error(request,"fiald")
    return redirect('loan_request_view')


def loan_request_reject(request, leave_id):
    if request.method == "POST":
        leave = LoanRequest.objects.get(id=leave_id)
        leave.leave_status = 2
        leave.reject_reason = request.POST.get('reject_reason')
        leave.save()
        return redirect('loan_request_view')
    else:
        # Render the reject form in the same template
        leave = LoanRequest.objects.get(id=leave_id)
        context = {
            'leave': leave
            }
        return render(request, 'loan_staff.html', context)


##################
def loan_request(request,customer_id):
    customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
    loan_request= LoanRequest.objects.all()
    cust = CustBalance.objects.filter(customer_id=customer_profile).count()
    
    result = True
    for loan in loan_request:
        print(loan.leave_status)
        if loan.customer_id == customer_profile and loan.leave_status != 2:
            result = False
    context = {
        "loan_request": loan_request,
        "customer_profile":customer_profile,
        "result": result,
        "cust": cust,
        
    }
    return render(request, "loan_request.html", context)



def loan_request_save(request):
    
    if request.method != "POST":
        messages.error(request, "Invalid Method")
    else:
        leave_date = request.POST.get('leave_date')
        customer_id = request.POST.get('id')
        customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
        loan_request= LoanRequest.objects.filter(customer_id=customer_profile)
        context = {
            "loan_request": loan_request,
            "customer_profile":customer_profile
        }
        try:
            loan_request1 = LoanRequest(customer_id=customer_profile, leave_status=0)
            loan_request1.save()
            messages.success(request, "Successful request")
            return redirect('/loan_request/'+customer_id)
        except:
            messages.error(request, "Failed to Apply Loan")
            return redirect('/loan_request/'+customer_id)

def continue_loan(request,customer_id):
    try:
        customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
        loan_req = LoanRequest.objects.get(customer_id=customer_profile,leave_status=1)
        if request.method == 'POST':
            loan_amount = int(request.POST.get('loan_amount' ,0))
            loan_id = request.POST.get('id')
            result = False
            if (
                loan_req.customer_id.willing_total <= 20000 
                and loan_amount <= loan_req.customer_id.willing_total * 5
                and loan_amount <= 80000
                ):
                result = True
                messages.success(request, "Your loan request has been approved. You will receive the money shortly.")
            elif (
                loan_req.customer_id.willing_total > 20000 
                and loan_req.customer_id.willing_total <= 30000  
                and loan_amount <= loan_req.customer_id.willing_total * 4
                and loan_amount <= 100000
                ):
                result = True
                messages.success(request, "Your loan request has been approved. You will receive the money shortly.")
            elif (
                loan_req.customer_id.willing_total > 30000 
                and loan_req.customer_id.willing_total <= 50000 
                and loan_amount <= loan_req.customer_id.willing_total * 3.5
                and loan_amount <= 150000
                ):
                result = True
                messages.success(request, "Your loan request has been approved. You will receive the money shortly.")
            elif (
                loan_req.customer_id.willing_total > 50000 
                and loan_req.customer_id.willing_total <= 75000 
                and loan_amount <= loan_req.customer_id.willing_total * 3
                and loan_amount <= 200000
                ):
                result = True
                messages.success(request, "Your loan request has been approved. You will receive the money shortly.")
            elif (
                loan_req.customer_id.willing_total > 75000 
                and loan_req.customer_id.willing_total <= 150000 
                and loan_amount <= loan_req.customer_id.willing_total * 2.7
                and loan_amount <= 350000
                ):
                result = True
                messages.success(request, "Your loan request has been approved. You will receive the money shortly.")
            elif (
                loan_req.customer_id.willing_total > 150000 
                and loan_amount <= loan_req.customer_id.willing_total * 2.4
                and loan_amount <= 500000
                ):
                result = True
                messages.success(request, "Your loan request has been approved. You will receive the money shortly.")
            else:
                messages.error(request, "Your balance is not enough to request this loan amount.")
            if result:
                try:
                    loan = LoanRequest.objects.get(id=loan_id)
                    loan.loan_amount = loan_amount
                    loan.leave_status = 3
                    loan.save()
                except:
                    messages.error(request, "error")
        context = {
            'loan_req': loan_req,
            'customer_name': customer_profile.user.first_name,
            'customer_willing_total': customer_profile.willing_total,
            'customer_profile': customer_profile
            
        }
        return render(request, 'continue_loan.html', context)
    except LoanRequest.DoesNotExist:
        messages.error(request, "Loan request does not exist.")
        return redirect('/loan_request/'+customer_id)


def loan_sub_view(request):
    loads = LoanRequest.objects.all()
    
    context = {
        "loads": loads
    }
    return render(request, 'cust_info.html', context)


def cont_loan_approve(request, loan_id):
    load = LoanRequest.objects.get(id=loan_id)
    load.leave_status = 1
    load.save()
    return redirect('loan_sub_view')


def cont_loan_reject(request, loan_id):
    if request.method == "POST":
        load = LoanRequest.objects.get(id=loan_id)
        print(id=loan_id)
        load.leave_status = 2
        load.save()
        return redirect('loan_sub_view')

def loan_approval_approve(request, loan_id):
    loan_request = LoanRequest.objects.get(id=loan_id)
    loan_request.leave_status = 1  # Set the status to "Approved"
    loan_request.save()
    return redirect('cust_info')

def admin_loan_approval_view(request):
    approval_requests = LoanRequest.objects.all()
    
    context = {
        'approval_requests': approval_requests,
    }
    return render(request, 'admin_loan_approval.html', context)


def admin_loan_approval_approve(request, approval_id):
    try:
        approval_request = LoanRequest.objects.get(id=approval_id)
        approval_request.leave_status = 4
        approval_request.save()
        admin_bal = AdminProfile.objects.all()
        for adm in admin_bal:
            adm.balance1 = adm.balance1 - approval_request.loan_amount
            adm.save()
        adm = Account.objects.get(customer_id=approval_request.customer_id)
        adm.account_balance= adm.account_balance + approval_request.loan_amount
        adm.save()
        messages.success(request,"Successfully Approved!")
    except:
        messages.error(request,"Failed to Approve.")
    return redirect('admin_loan_approval_view')


def admin_loan_approval_reject(request, approval_id):
    approval_request = LoanRequest.objects.get(id=approval_id)
    approval_request.leave_status = 5
    approval_request.save()
    return redirect('admin_loan_approval_view')



















def search_cust(request):
    query = request.GET.get('q')  

    if query:
        customers = CustomerProfile.objects.filter(customer_id=query)
    else:
        customers = CustomerProfile.objects.all() 

    context = {
        'customers': customers,
        'query': query
    }
    return render(request, 'cust_search.html', context)

def bal_admin(request):
    ban=AdminProfile.objects.all()
    
    context={
        "ban": ban
        
    }
    return render(request, 'bal_admin.html',context)


def report(request):
    
    return render(request, 'report.html')

def approve_report(request):
    return render(request, 'approve_report.html')

def manage_pro(request):
    cu = Customer.objects.all()
    cu1=CustomerProfile.objects.all()
    
    context = {
        "cu": cu,'cu1':cu1
}
    return render(request, "manage_pro.html", context)

def update_profile(request,customer_id):
    
    customer_profile=CustomerProfile.objects.get(customer_id=customer_id)
    cu = Customer.objects.get(id=customer_profile.user.id)
    cust = CustBalance.objects.filter(customer_id=customer_profile).count()
    loan_request=LoanRequest.objects.all()
    # ac=Account.objects.
    context = {
        "cu": cu,
        "customer_id": customer_id,
        'customer_profile': customer_profile,
        'cust':cust,
        # 'loan_r':loan_r,
    }
    return render(request, "edit_cust.html", context)

def update_profile_save(request):
    
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        customer_id = request.POST.get('customer_id_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        phone_no = request.POST.get('phone_no')
        department = request.POST.get('department')
        salary_p = request.POST.get('salary_p')
        # pass1 = request.POST.get('password1')
        # pass2 = request.POST.get('password2')
        # account = request.POST.get('account')
        print(customer_id)
        try:
            # INSERTING into Customuser Model
            loan_request=LoanRequest.objects.all()
            customer_profile=CustomerProfile.objects.get(customer_id=customer_id)
            cust = CustBalance.objects.filter(customer_id=customer_profile).count()
            user = Customer.objects.get(id=customer_profile.user.id)
            
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            customer_profile=CustomerProfile.objects.get(customer_id=customer_id)
            customer_profile.address=address
            customer_profile.sex=sex
            customer_profile.age=age
            customer_profile.phone_no=phone_no
            customer_profile.department=department
            customer_profile.salary_p=salary_p
            customer_profile.save()
            
            context = {
                'customer_id': customer_id,
                'message': 'Customer Updated Successfully.',
                'message_type': 'success',
                'cust':cust,
                'loan_request':loan_request
            }
            return render(request, "edit_cust.html", context)

        except:
            # Add error message to the context
            context = {
                'customer_id': customer_id,
                'message': 'Failed to Update Staff.',
                'message_type': 'error',
                'loan_request':loan_request
            }
            return render(request, "cust_home.html", context)
    

def account_view(request):
    if request.method == 'POST':
        account_no = request.POST.get('account')
        password = request.POST.get('pass')
    
        
        user = authenticate(request, username=account_no, password=password)
        
        
        print(user)
        
        if user is not None:
            login(request, user)
            return redirect('account_view1')  
        else:
            messages.error(request, 'Invalid account number or password.')
    
    return render(request, 'account_view.html')


@login_required
def account_view1(request):
    customer = Account.objects.get(user=request.user)
    return render(request, 'account_view1.html', {'customer': customer})


def payment(request,customer_id):
    customer_profile = CustomerProfile.objects.get(customer_id=customer_id)
    loan_request = LoanRequest.objects.filter(customer_id=customer_profile )
    cust = CustBalance.objects.filter(customer_id=customer_profile).count()
    acc=Account.objects.get(customer_id=customer_profile) 
    adm = AdminProfile.objects.all()
    context={
            'loan_request':loan_request,
            'cust': cust,
            'customer_profile':customer_profile 
            }
    return render (request,'payment.html',context)
    
def payment_save(request):
    if request.method == "POST":
        pay=int(request.POST.get('payment'))
        pay_id = request.POST.get('id')
        loan_request = LoanRequest.objects.all()
        for loan_req in loan_request:
            if int(loan_req.customer_id.customer_id) == int(pay_id):
                print(pay_id)
                if loan_req.loan_amount == pay and pay > 0 :
                    acc = Account.objects.get(customer_id=loan_req.customer_id)
                    acc.account_balance -= pay 
                    acc.save()
                    loan = LoanRequest.objects.get(customer_id=loan_req.customer_id)
                    loan.loan_amount -= pay
                    loan.save()
                    adm = AdminProfile.objects.all()
                    for a in adm:
                        a.balance1+= pay
                        a.save()
                    messages.success(request, "Your Payment is Sucessful!") 
                    return redirect('/payment/'+pay_id)
                else:
                    messages.error(request, "Your Money is Insufficent")
                    return redirect('/payment/'+pay_id) 

    else:
        messages.error(request, "error") 
    context={
        'loan_request':loan_request,
    }
    return redirect('/payment/'+pay_id)
    
# def password_reset(request):
#     custo = Customer.objects.get(id=request.user.id)
    
#     return render(request, "password_reset.html")

# def password_reset_save(request):
#     if request.method != "POST":
#         messages.error(request, "Method Not Allowed!")
#         return redirect('password_reset.html')
#     else:
#         username = request.POST.get('username')
#         user_id = request.POST.get('user_id')
#         email = request.POST.get('email')
#         new_pass = request.POST.get('new_pass')
#         con_pass = request.POST.get('con_pass')
#         custo = Customer.objects.get(id=request.user.id)
#         try:
#             for cu in custo:
#                 if username == cu.username and email == cu.email:
#                     if new_pass == con_pass and new_pass != None and new_pass != "":
#                         print(user.admin.password)
#                         user.admin.set_password(new_pass)
#                         cu.save()
#                         print(user.admin.password)
#                         messages.success(request, "Password Update Successfully")
#                         return redirect('/login')
#                     else :
#                         messages.error(request, "The Password are Different")
#                         return redirect('password_reset')
#                 else:
#                     messages.error(request, "Invalid Username or ID or Email")
#                     return redirect('password_reset')
#         except:
#             messages.error(request, "Faild to Update Password")
#             return redirect('/login')
        
        