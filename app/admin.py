from django.contrib import admin
from .models import data, act,CustomerProfile, AdminProfile, Admin2Profile, FinanceProfile, StaffProfile,Dilla_emp,LoanRequest,AdminProfile,CustBalance,Account,LeaveReportCustomer,LeaveReportStaff
admin.site.register(data)
admin.site.register(act)
admin.site.register(Dilla_emp)


# class CustomerProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'customer_id', 'department', 'salary')
#     search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'customer_id')
#     list_filter = ('department', 'salary')


# admin.site.register(act, UserAdmin)
admin.site.register(CustomerProfile), #CustomerProfileAdmin)
# admin.site.register(AdminProfile)
# admin.site.register(Admin2Profile)
admin.site.register(FinanceProfile)
admin.site.register(StaffProfile)
admin.site.register(LoanRequest)
admin.site.register(AdminProfile)
admin.site.register(CustBalance)
admin.site.register(Account)
admin.site.register(LeaveReportCustomer)
admin.site.register(LeaveReportStaff)
