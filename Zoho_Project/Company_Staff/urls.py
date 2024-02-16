from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------Company section--------------------------------
    path('Company/Dashboard',views.company_dashboard,name='company_dashboard'),
    path('Company/Staff-Request',views.company_staff_request,name='company_staff_request'),
    path('Company/Staff-Request/Accept/<int:pk>',views.staff_request_accept,name='staff_request_accept'),
    path('Company/Staff-Request/Reject/<int:pk>',views.staff_request_reject,name='staff_request_reject'),
    path('Company/All-Staffs',views.company_all_staff,name='company_all_staff'),
    path('Company/Staff-Approval/Cancel/<int:pk>',views.staff_approval_cancel,name='staff_approval_cancel'),
    path('Company/Profile',views.company_profile,name='company_profile'),
    path('Company/Profile-Editpage',views.company_profile_editpage,name='company_profile_editpage'),
    path('Company/Profile/Edit/Basicdetails',views.company_profile_basicdetails_edit,name='company_profile_basicdetails_edit'),
    path('Company/Password_Change',views.company_password_change,name='company_password_change'),
    path('Company/Profile/Edit/Companydetails',views.company_profile_companydetails_edit,name='company_profile_companydetails_edit'),
    path('Company/Module-Editpage',views.company_module_editpage,name='company_module_editpage'),
    path('Company/Module-Edit',views.company_module_edit,name='company_module_edit'),
    path('Company/Renew/Payment_terms',views.company_renew_terms,name='company_renew_terms'),
    
    
    
     # -------------------------------Attendance section--------------------------------
    path('company_attendance_list',views.company_attendance_list,name='company_attendance_list'),
    path('company_mark_attendance',views.company_mark_attendance,name='company_mark_attendance'),
    path('add_attendance',views.add_attendance,name='add_attendance'),
    path('attendance_calendar/<int:employee_id>/<int:target_year>/<int:target_month>/',views.attendance_calendar,name='attendance_calendar'),
    path('add_comment',views.add_comment,name='add_comment'),
    path('delete_comment/<int:id>',views.delete_attendance_comment,name='delete_comment'),
    path('attendance_overview/<int:employee_id>/<int:target_month>/<int:target_year>/',views.attendance_overview,name='attendance_overview'),
    path('attendance_pdf/<int:employee_id>/<int:target_month>/<int:target_year>',views.attendance_pdf,name='attendance_pdf'),
    path('attendance_email/<int:employee_id>/<int:target_month>/<int:target_year>',views.attendance_email,name='attendance_email'),
    path('attendance_edit/<int:id>',views.attendance_edit,name='attendance_edit'),
    path('edit_attendance/<int:id>',views.edit_attendance,name='edit_attendance'),
    path('attendance_delete/<int:id>',views.attendance_delete,name='attendance_delete'),
    path('attendance_add_blood',views.attendance_add_blood,name='attendance_add_blood'),
    path('attendance_create_employee',views.attendance_create_employee,name='attendance_create_employee'),
    path('attendance_import',views.attendance_import,name='attendance_import'),
    # -------------------------------Staff section--------------------------------
    path('Staff/Dashboard',views.staff_dashboard,name='staff_dashboard'),
    path('Staff/Profile',views.staff_profile,name='staff_profile'),
    path('Staff/Profile-Editpage',views.staff_profile_editpage,name='staff_profile_editpage'),
    path('Staff/Profile/Edit/details',views.staff_profile_details_edit,name='staff_profile_details_edit'),
    path('Staff/Password_Change',views.staff_password_change,name='staff_password_change'),



    # -------------------------------Zoho Modules section--------------------------------
  
    
]