from django.urls import path, include
from . import views

urlpatterns = [

    path("signup/", views.SignupPage, name="signup"),
    path("login/", views.LoginPage, name="login"),
    path("about_page/", views.about_page, name="about_page"),
    path("contact_us/", views.contact_us, name="contact_us"),
    # path("login1/", views.LoginPage1, name="login1"),
    # path('get_user_details/', views.get_user_details, name="get_user_details"),
    path("admin_home/", views.HomePage, name="admin_home"),
    path("admin2_home/", views.admin2_home, name="admin2_home"),
    path("cust_home/<int:customer_id>/", views.cust_home, name="cust_home"),
    path("finance_home/", views.finance_home, name="finance_home"),
    ######staff#########
    path("staff_home/", views.staff_home, name="staff_home"),
    path('add_staff/',views.add_staff,name='add_staff'),
    path('add_staff_save/',views.add_staff_save,name='add_staff_save'),
    path('manage_staff/',views.manage_staff,name='manage_staff'),
    path('edit_staff/<staff_id>/', views.edit_staff, name="edit_staff"),
    path('edit_staff_save/', views.edit_staff_save, name="edit_staff_save"),
    path('update_profile/<int:customer_id>/', views.update_profile, name="update_profile"),
    path('update_profile_save/', views.update_profile_save, name="update_profile_save"),
    path('manage_pro/', views.manage_pro, name='manage_pro'),
    path('delete_staff/<staff_id>/', views.delete_staff, name="delete_staff"),
    # path('search_staff/', views.search_staff, name="search_staff"),
    ################
    path("logout/", views.LogoutPage, name="logout"),
    path("", views.FrontPage, name="front"),
    path("check_balance/<customer_id>/", views.check_balance1, name="check_balance"),
    path("dilla_emp/", views.dilla_emp, name="dilla_emp"),
    path('dilla_emp/update/', views.update_dilla_emp, name='update'),
    path('dilla_emp/update/update_record/<int:id>/', views.update_record, name='update_record'),
    path("deposit/<customer_id>/", views.deposit_money, name="deposit"),
    path("withdraw/<customer_id>/", views.withdraw, name="withdraw"),
    # path("account_view", views.account_view, name="account_view"),
    # path("account_view1/<int:customer_id>", views.account_view, name="account_view"),
    #######staff leave######
    path('staff_leave/', views.staff_leave, name="staff_leave"),
    path('staff_leave_save/', views.staff_leave_save, name="staff_leave_save"),
    #######staff leave view######
    path('staff_leave_view/', views.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', views.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', views.staff_leave_reject, name="staff_leave_reject"),
    #######cust leave ###### 
    path('cust_leave/<customer_id>/', views.cust_leave, name="cust_leave"),
    path('cust_leave_save/', views.cust_leave_save, name="cust_leave_save"),
    #######cust leave view######
    path('cust_leave_view/', views.cust_leave_view, name="cust_leave_view"),
    path('cust_leave_approve/<leave_id>/', views.cust_leave_approve, name="cust_leave_approve"),
    path('cust_leave_reject/<leave_id>/',views.cust_leave_reject, name="cust_leave_reject"),
    #######cust complain######
    path("cust_complain/<customer_id>/", views.cust_complain, name="cust_complain"),
    path('cust_complain_save/', views.cust_complain_save, name="cust_complain_save"),
    #######cust complain reply######
    path('cust_complain_message/', views.cust_complain_message, name='cust_complain_message'),
    path('cust_complain_reply/', views.cust_complain_reply, name="cust_complain_reply"),
    # path('admin_complain',views.admin_complain, name="admin_complain"),
    ###########Transfer money############
    path('transfer_money/',views.transfer_money, name="transfer_money"),
    path('transfer_money_save/',views.transfer_money_save, name="transfer_money_save"),
    path('finance_info/', views.finance_info, name='finance_info'),
    ##############loan request#####
    path('loan_request/<customer_id>/', views.loan_request, name="loan_request"),
    path('loan_request_save/', views.loan_request_save, name="loan_request_save"),
    path('loan_request_view/', views.loan_request_view, name="loan_request_view"),
    path('loan_request_approve/<leave_id>/', views.loan_request_approve, name="loan_request_approve"),
    path('loan_request_reject/<leave_id>/', views.loan_request_reject, name="loan_request_reject"),
    path('continue_loan/<customer_id>/', views.continue_loan, name='continue_loan'),
    path('loan_sub_view/', views.loan_sub_view, name="loan_sub_view"),
    path('cont_loan_approve/<loan_id>/', views.cont_loan_approve, name="cont_loan_approve"),
    path('cont_loan_reject/<loan_id>/', views.cont_loan_reject, name="cont_loan_reject"),
    path('admin_loan_approval_view/', views.admin_loan_approval_view, name='admin_loan_approval_view'),
    path('admin_loan_approval_approve<int:approval_id>/', views.admin_loan_approval_approve, name='admin_loan_approval_approve'),
    path('admin_loan_approval_reject<int:approval_id>/', views.admin_loan_approval_reject, name='admin_loan_approval_reject'),
    path('loan_approval_approve/<int:loan_id>/', views.loan_approval_approve, name='loan_approval_approve'),

    path('bal_admin/', views.bal_admin, name="bal_admin"),
    path('search_cust/', views.search_cust, name="search_cust"),
    path('view_bal/<customer_id>/',views.view_bal,name="view_bal"),
    path('approve_report', views.approve_report, name="approve_report"),

    path('account_view/', views.account_view, name='account_view'),
    path('account_view1/', views.account_view1, name='account_view1'),
    # path('calculate_interest/<int:customer_id>/', views.calculate_interest, name='calculate_interest'),
    path('payment/<customer_id>/', views.payment, name='payment'),
    path('payment_save/', views.payment_save, name='payment_save'),
    # path('password_reset', views.password_reset, name='password_reset'),
    # path('password_reset_save/', views.password_reset_save, name='password_reset_save'),
]

    