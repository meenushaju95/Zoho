from django.shortcuts import render,redirect,HttpResponse
from Register_Login.models import *
from Register_Login.views import logout
from django.contrib import messages
from django.conf import settings
from datetime import date
from datetime import datetime, timedelta
from .models import payroll_employee,Attendance,Attendance_History,Holiday,Attendance_comment
from django.shortcuts import get_object_or_404
from datetime import datetime,timedelta
from calendar import monthrange
from collections import defaultdict
from django.db.models import Q
import calendar





# Create your views here.



# -------------------------------Company section--------------------------------

# company dashboard
def company_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')

        # Calculate the date 20 days before the end date for payment term renew
        reminder_date = dash_details.End_date - timedelta(days=20)
        current_date = date.today()
        alert_message = current_date >= reminder_date

        # Calculate the number of days between the reminder date and end date
        days_left = (dash_details.End_date - current_date).days
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'alert_message':alert_message,
            'days_left':days_left,
        }
        return render(request, 'company/company_dash.html', context)
    else:
        return redirect('/')


# company staff request for login approval
def company_staff_request(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        staff_request=StaffDetails.objects.filter(company=dash_details.id, company_approval=0).order_by('-id')
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'requests':staff_request,
        }
        return render(request, 'company/staff_request.html', context)
    else:
        return redirect('/')

# company staff accept or reject
def staff_request_accept(request,pk):
    staff=StaffDetails.objects.get(id=pk)
    staff.company_approval=1
    staff.save()
    return redirect('company_staff_request')

def staff_request_reject(request,pk):
    staff=StaffDetails.objects.get(id=pk)
    login_details=LoginDetails.objects.get(id=staff.company.id)
    login_details.delete()
    staff.delete()
    return redirect('company_staff_request')


# All company staff view, cancel staff approval
def company_all_staff(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        all_staffs=StaffDetails.objects.filter(company=dash_details.id, company_approval=1).order_by('-id')
       
        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'staffs':all_staffs,
        }
        return render(request, 'company/all_staff_view.html', context)
    else:
        return redirect('/')

def staff_approval_cancel(request, pk):
    """
    Sets the company approval status to 2 for the specified staff member, effectively canceling staff approval.

    This function is designed to be used for canceling staff approval, and the company approval value is set to 2.
    This can be useful for identifying resigned staff under the company in the future.

    """
    staff = StaffDetails.objects.get(id=pk)
    staff.company_approval = 2
    staff.save()
    return redirect('company_all_staff')


# company profile, profile edit
def company_profile(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        terms=PaymentTerms.objects.all()

        # Calculate the date 20 days before the end date
        reminder_date = dash_details.End_date - timedelta(days=20)
        current_date = date.today()
        renew_button = current_date >= reminder_date

        context = {
            'details': dash_details,
            'allmodules': allmodules,
            'renew_button': renew_button,
            'terms':terms,
        }
        return render(request, 'company/company_profile.html', context)
    else:
        return redirect('/')

def company_profile_editpage(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'company/company_profile_editpage.html', context)
    else:
        return redirect('/')

def company_profile_basicdetails_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        if request.method == 'POST':
            # Get data from the form
            log_details.first_name = request.POST.get('fname')
            log_details.last_name = request.POST.get('lname')
            log_details.email = request.POST.get('eid')
            log_details.username = request.POST.get('uname')
            log_details.save()
            messages.success(request,'Updated')
            return redirect('company_profile_editpage') 
        else:
            return redirect('company_profile_editpage') 

    else:
        return redirect('/')
    
def company_password_change(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        if request.method == 'POST':
            # Get data from the form
            password = request.POST.get('pass')
            cpassword = request.POST.get('cpass')
            if password == cpassword:
                log_details.password=password
                log_details.save()

            messages.success(request,'Password Changed')
            return redirect('company_profile_editpage') 
        else:
            return redirect('company_profile_editpage') 

    else:
        return redirect('/')
       
def company_profile_companydetails_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details = LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)

        if request.method == 'POST':
            # Get data from the form
            gstno = request.POST.get('gstno')
            profile_pic = request.FILES.get('image')

            # Update the CompanyDetails object with form data
            dash_details.company_name = request.POST.get('cname')
            dash_details.contact = request.POST.get('phone')
            dash_details.address = request.POST.get('address')
            dash_details.city = request.POST.get('city')
            dash_details.state = request.POST.get('state')
            dash_details.country = request.POST.get('country')
            dash_details.pincode = request.POST.get('pincode')
            dash_details.pan_number = request.POST.get('pannumber')

            if gstno:
                dash_details.gst_no = gstno

            if profile_pic:
                dash_details.profile_pic = profile_pic

            dash_details.save()

            messages.success(request, 'Updated')
            return redirect('company_profile_editpage')
        else:
            return redirect('company_profile_editpage')
    else:
        return redirect('/')    

# company modules editpage
def company_module_editpage(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'company/company_module_editpage.html', context)
    else:
        return redirect('/')

def company_module_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details,status='New')

        if request.method == 'POST':
            # Retrieve values
            items = request.POST.get('items', 0)
            price_list = request.POST.get('price_list', 0)
            stock_adjustment = request.POST.get('stock_adjustment', 0)
            godown = request.POST.get('godown', 0)

            cash_in_hand = request.POST.get('cash_in_hand', 0)
            offline_banking = request.POST.get('offline_banking', 0)
            upi = request.POST.get('upi', 0)
            bank_holders = request.POST.get('bank_holders', 0)
            cheque = request.POST.get('cheque', 0)
            loan_account = request.POST.get('loan_account', 0)

            customers = request.POST.get('customers', 0)
            invoice = request.POST.get('invoice', 0)
            estimate = request.POST.get('estimate', 0)
            sales_order = request.POST.get('sales_order', 0)
            recurring_invoice = request.POST.get('recurring_invoice', 0)
            retainer_invoice = request.POST.get('retainer_invoice', 0)
            credit_note = request.POST.get('credit_note', 0)
            payment_received = request.POST.get('payment_received', 0)
            delivery_challan = request.POST.get('delivery_challan', 0)

            vendors = request.POST.get('vendors', 0)
            bills = request.POST.get('bills', 0)
            recurring_bills = request.POST.get('recurring_bills', 0)
            vendor_credit = request.POST.get('vendor_credit', 0)
            purchase_order = request.POST.get('purchase_order', 0)
            expenses = request.POST.get('expenses', 0)
            recurring_expenses = request.POST.get('recurring_expenses', 0)
            payment_made = request.POST.get('payment_made', 0)

            projects = request.POST.get('projects', 0)

            chart_of_accounts = request.POST.get('chart_of_accounts', 0)
            manual_journal = request.POST.get('manual_journal', 0)

            eway_bill = request.POST.get('ewaybill', 0)

            employees = request.POST.get('employees', 0)
            employees_loan = request.POST.get('employees_loan', 0)
            holiday = request.POST.get('holiday', 0)
            attendance = request.POST.get('attendance', 0)
            salary_details = request.POST.get('salary_details', 0)

            reports = request.POST.get('reports', 0)

            update_action=1
            status='Pending'

            # Create a new ZohoModules instance and save it to the database
            data = ZohoModules(
                company=dash_details,
                items=items, price_list=price_list, stock_adjustment=stock_adjustment, godown=godown,
                cash_in_hand=cash_in_hand, offline_banking=offline_banking, upi=upi, bank_holders=bank_holders,
                cheque=cheque, loan_account=loan_account,
                customers=customers, invoice=invoice, estimate=estimate, sales_order=sales_order,
                recurring_invoice=recurring_invoice, retainer_invoice=retainer_invoice, credit_note=credit_note,
                payment_received=payment_received, delivery_challan=delivery_challan,
                vendors=vendors, bills=bills, recurring_bills=recurring_bills, vendor_credit=vendor_credit,
                purchase_order=purchase_order, expenses=expenses, recurring_expenses=recurring_expenses,
                payment_made=payment_made,
                projects=projects,
                chart_of_accounts=chart_of_accounts, manual_journal=manual_journal,
                eway_bill=eway_bill,
                employees=employees, employees_loan=employees_loan, holiday=holiday,
                attendance=attendance, salary_details=salary_details,
                reports=reports,update_action=update_action,status=status    
            )
            data.save()
            messages.info(request,"Request sent successfully. Please wait for approval.")
            return redirect('company_module_editpage')
        else:
            return redirect('company_module_editpage')  
    else:
        return redirect('/')


def company_renew_terms(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = CompanyDetails.objects.get(login_details=log_details,superadmin_approval=1,Distributor_approval=1)
        if request.method == 'POST':
            select=request.POST['select']
            terms=PaymentTerms.objects.get(id=select)
            update_action=1
            status='Pending'
            newterms=PaymentTermsUpdates(
               company=dash_details,
               payment_term=terms,
               update_action=update_action,
               status=status 
            )
            newterms.save()
            messages.success(request,'Successfully requested an extension of payment terms. Please wait for approval.')
            return redirect('company_profile')
    else:
        return redirect('/')









# -------------------------------Staff section--------------------------------

# staff dashboard
def staff_dashboard(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
        }
        return render(request,'staff/staff_dash.html',context)
    else:
        return redirect('/')


# staff profile
def staff_profile(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context={
            'details':dash_details,
            'allmodules': allmodules,
        }
        return render(request,'staff/staff_profile.html',context)
    else:
        return redirect('/')


def staff_profile_editpage(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        allmodules= ZohoModules.objects.get(company=dash_details.company,status='New')
        context = {
            'details': dash_details,
            'allmodules': allmodules
        }
        return render(request, 'staff/staff_profile_editpage.html', context)
    else:
        return redirect('/')

def staff_profile_details_edit(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        dash_details = StaffDetails.objects.get(login_details=log_details,company_approval=1)
        if request.method == 'POST':
            # Get data from the form
            log_details.first_name = request.POST.get('fname')
            log_details.last_name = request.POST.get('lname')
            log_details.email = request.POST.get('eid')
            log_details.username = request.POST.get('uname')
            log_details.save()
            dash_details.contact = request.POST.get('phone')
            old=dash_details.image
            new=request.FILES.get('profile_pic')
            print(new,old)
            if old!=None and new==None:
                dash_details.image=old
            else:
                print(new)
                dash_details.image=new
            dash_details.save()
            messages.success(request,'Updated')
            return redirect('staff_profile_editpage') 
        else:
            return redirect('staff_profile_editpage') 

    else:
        return redirect('/')

def staff_password_change(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')

        log_details= LoginDetails.objects.get(id=log_id)
        if request.method == 'POST':
            # Get data from the form
            password = request.POST.get('pass')
            cpassword = request.POST.get('cpass')
            if password == cpassword:
                log_details.password=password
                log_details.save()

            messages.success(request,'Password Changed')
            return redirect('staff_profile_editpage') 
        else:
            return redirect('staff_profile_editpage') 

    else:
        return redirect('/')
    


# -------------------------------Attendance section--------------------------------
    
def get_days_in_month(target_year, target_month):
    _, days_in_month = monthrange(target_year, target_month)
    days = [day for day in range(1, days_in_month + 1)]
    return days
def calculate_leave_count(employee, target_month, target_year):
    return Attendance.objects.filter(employee=employee, date__month =target_month, date__year=target_year).count()
def calculate_holiday_count(company, target_month, target_year):
    _, last_day = monthrange(target_year, target_month)
    first_day_of_month = datetime(target_year, target_month, 1)
    last_day_of_month = datetime(target_year, target_month, last_day) + timedelta(days=1)  # Add one day to include the entire end day

    holidays = Holiday.objects.filter(
        start_date__lt=last_day_of_month,
        end_date__gte=first_day_of_month,
        company=company,
    )

    count = 0
    for day in range(1, last_day + 1):
        target_date = datetime(target_year, target_month, day)
        if holidays.filter(start_date__lte=target_date, end_date__gte=target_date).exists():
            count += 1

    return count

   
def company_attendance_list(request):
        
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details = LoginDetails.objects.get(id=log_id)

        if log_details.user_type == 'Staff':
            staff = StaffDetails.objects.get(login_details=log_details)
            items = Attendance.objects.filter(company=staff.company)
                
        elif log_details.user_type == 'Company':
            company = CompanyDetails.objects.get(login_details=log_details)
            items = Attendance.objects.filter(company=company)
             

        consolidated_entries = defaultdict(list)

        for item in items:
            target_month = item.date.month
            target_year = item.date.year
            employee_id = item.employee.id

            leave_count = calculate_leave_count(item.employee, target_month, target_year)

            existing_entry = next(
                (
                    entry
                    for entry in consolidated_entries[employee_id]
                    if entry['target_month'] == target_month and entry['target_year'] == target_year
                ),
                None,
            )

            if existing_entry:
                existing_entry['leave'] += leave_count
            else:
                MONTH_NAMES = {
                    1: 'January',
                    2: 'February',
                    3: 'March',
                    4: 'April',
                    5: 'May',
                    6: 'June',
                    7: 'July',
                    8: 'August',
                    9: 'September',
                    10: 'October',
                    11: 'November',
                    12: 'December'
                }

                entry = {
                    'employee': item.employee,
                    'target_month': target_month,
                    'target_month_name': MONTH_NAMES.get(target_month, ''),
                    'target_year': target_year,
                    'working_days': len(get_days_in_month(target_year, target_month)),
                    'holidays': calculate_holiday_count(item.company, target_month, target_year),
                    'leave': leave_count,
                    'work_days': len(get_days_in_month(target_year, target_month)) - calculate_holiday_count(item.company, target_month, target_year) - leave_count,
                    'total_leave': leave_count,
                }

                consolidated_entries[employee_id].append(entry)

        all_entries = []
        for employee_id, entries in consolidated_entries.items():
            for entry in entries:
                all_entries.append(entry)
        employee_ids = [entry['employee'].id for entries in consolidated_entries.values() for entry in entries]
        employee_ids = [int(id) for id in employee_ids]  # Convert IDs to integers
        request.session['employee_ids'] = employee_ids
        print(employee_ids)

        return render(request, 'Attendance/company_attendance_list.html', {
            'all_entries': all_entries,
            'month_name': MONTH_NAMES
        })
            
def company_mark_attendance(request):
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details = LoginDetails.objects.get(id=log_id)
        if log_details.user_type == 'Company':
            
            employee = payroll_employee.objects.filter(login_details=log_details,status='Active')
            return render(request,'Attendance/company_mark_attendance.html',{'staffs':employee})
        if log_details.user_type=='Staff':
            staff = StaffDetails.objects.get(login_details=log_details)
            
            employee = payroll_employee.objects.filter(company=staff.company,status='Active')
            return render(request,'Attendance/company_mark_attendance.html',{'staffs':employee})
        
def add_attendance(request):
        if request.method == 'POST':
            emp_id = request.POST['employee']
        date = request.POST['date']
        status = request.POST['status']
        reason = request.POST['reason']

        if 'login_id' in request.session:
            log_id = request.session['login_id']
            log_details = LoginDetails.objects.get(id=log_id)

            if log_details.user_type == 'Company':
                employee = get_object_or_404(payroll_employee, id=emp_id, login_details=log_details)
                company = CompanyDetails.objects.get(login_details=log_details)
            elif log_details.user_type == 'Staff':
                staff = StaffDetails.objects.get(login_details=log_details)
                employee = get_object_or_404(payroll_employee, id=emp_id, company=staff.company)
                company = staff.company

            is_holiday = Holiday.objects.filter(company=company, start_date__lte=date, end_date__gte=date).exists()

            if is_holiday:
                messages.warning(request, 'Selected date is a company holiday.')
                return redirect('company_mark_attendance')
            

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=date,
                defaults={'status': status, 'reason': reason, 'company': company, 'login_details': log_details}
            )

            if not created:
                # Update the existing attendance if it already exists for the specified date
                attendance.status = status
                attendance.reason = reason
           
                attendance.save()

            messages.success(request, 'Leave Marked')
            return redirect('company_mark_attendance')

def attendance_calendar(request, employee_id, target_year, target_month):
    calendar_data = {
        'employee_id': employee_id,
        'target_year': target_year,
        'target_month': target_month,
       
    }
    comment = Attendance_comment.objects.filter(month=target_month,year=target_year,employee=employee_id)
    employee_attendance = Attendance.objects.filter(
        employee_id=employee_id,
        date__year=target_year,
        date__month=target_month
    ).values('status', 'date')  # Fetch only the required fields
    
    employee=payroll_employee.objects.get(id=employee_id)
    target_month = max(1, min(target_month, 12))

# Calculate the next month and year if target_month is December
    next_month = 1 if target_month == 12 else target_month + 1
    next_year = target_year + 1 if target_month == 12 else target_year

# Construct the date strings for the start and end of the month
    start_date = datetime(target_year, target_month, 1).date()
    end_date = datetime(next_year, next_month, 1).date() - timedelta(days=1)
    
    holidays = Holiday.objects.filter(
    Q(company=employee.company) & (
    (Q(start_date__lte=end_date) & Q(end_date__gte=start_date)))  # Holidays overlapping the target month
    
)   
   
    # for getting atendance list
    if 'login_id' in request.session:
        log_id = request.session['login_id']
        if 'login_id' not in request.session:
            return redirect('/')
        log_details = LoginDetails.objects.get(id=log_id)

        if log_details.user_type == 'Staff':
            staff = StaffDetails.objects.get(login_details=log_details)
            items = Attendance.objects.filter(company=staff.company)
                
        elif log_details.user_type == 'Company':
            company = CompanyDetails.objects.get(login_details=log_details)
            items = Attendance.objects.filter(company=company)
             

        consolidated_entries = defaultdict(list)

        for item in items:
            target_month = item.date.month
            target_year = item.date.year
            employee_id = item.employee.id

            leave_count = calculate_leave_count(item.employee, target_month, target_year)

            existing_entry = next(
                (
                    entry
                    for entry in consolidated_entries[employee_id]
                    if entry['target_month'] == target_month and entry['target_year'] == target_year
                ),
                None,
            )

            if existing_entry:
                existing_entry['leave'] += leave_count
            else:
                MONTH_NAMES = {
                    1: 'January',
                    2: 'February',
                    3: 'March',
                    4: 'April',
                    5: 'May',
                    6: 'June',
                    7: 'July',
                    8: 'August',
                    9: 'September',
                    10: 'October',
                    11: 'November',
                    12: 'December'
                }

                entry = {
                    'employee': item.employee,
                    'target_month': target_month,
                    'target_month_name': MONTH_NAMES.get(target_month, ''),
                    'target_year': target_year,
                    'working_days': len(get_days_in_month(target_year, target_month)),
                    'holidays': calculate_holiday_count(item.company, target_month, target_year),
                    'leave': leave_count,
                    'work_days': len(get_days_in_month(target_year, target_month)) - calculate_holiday_count(item.company, target_month, target_year) - leave_count,
                    'total_leave': leave_count,
                }

                consolidated_entries[employee_id].append(entry)

        all_entries = []
        for employee_id, entries in consolidated_entries.items():
            for entry in entries:
                
                all_entries.append(entry)
   
    
    return render(request, 'Attendance/attendance_overview.html', {'emp_attendance': employee_attendance,'holiday':holidays,'entries':all_entries,'employee':employee,'comments':comment,'calendar_data':calendar_data})

def add_comment(request):
    if request.method == 'POST':
        if 'login_id' in request.session:
            log_id = request.session['login_id']
            if 'login_id' not in request.session:
                return redirect('/')
            log_details = LoginDetails.objects.get(id=log_id)

            if log_details.user_type == 'Staff':
                staff = StaffDetails.objects.get(login_details=log_details)
                company = staff.company
                    
            elif log_details.user_type == 'Company':
                company = CompanyDetails.objects.get(login_details=log_details)
            
            employe = request.POST['employee']
            emp=payroll_employee.objects.get(id=employe)
            
            target_month = request.POST['target_month']
            target_year = request.POST['target_year']
            comment = request.POST.get('comment')
            print(employe,target_month,target_year)
            comment = Attendance_comment(
                comment=comment,
                employee=emp,
                month=target_month,
                year=target_year, 
                company=company,
                login_details=log_details
               
            )
            comment.save()
            return redirect('attendance_calendar', employee_id=employe, target_year=target_year, target_month=target_month)
           
def delete_attendance_comment(request,id):
    comment = Attendance_comment.objects.get(id=id)    
    comment.delete()  
    return redirect('attendance_calendar', employee_id=comment.employee.id, target_year=comment.year, target_month=comment.month)       
                
                
                    
                        




        
        
    







# -------------------------------Zoho Modules section--------------------------------