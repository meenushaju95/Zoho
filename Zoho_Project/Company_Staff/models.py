from django.db import models
from Register_Login.models import*

# Create your models here.

#---------------- models for zoho modules--------------------
class payroll_employee(models.Model):
    title = models.CharField(max_length=100,null=True)
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    alias = models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to="image/", null=True)
    joindate=models.DateField(null=True)
    salary_type = models.CharField(max_length=100, default='Fixed',null=True)
    salary = models.IntegerField(null=True,blank=True)
    emp_number = models.CharField(max_length=100,null=True)
    designation = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=100,null=True)
    gender = models.CharField(max_length=100,null=True)
    dob=models.DateField(null=True)
    age = models.PositiveIntegerField(default=0)
    blood = models.CharField(max_length=10,null=True)
    parent = models.CharField(max_length=100,null=True)
    spouse_name = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=250,null=True)
    permanent_address = models.CharField(max_length=250,null=True)
    Phone = models.BigIntegerField(null=True)
    emergency_phone = models.BigIntegerField(null=True ,blank=True,default=1)
    email = models.EmailField(max_length=255,null=True)
    Income_tax_no = models.CharField(max_length=255,null=True)
    Aadhar = models.CharField(max_length=250,default='',null=True)
    UAN = models.CharField(max_length=255,null=True)
    PFN = models.CharField(max_length=255,null=True)
    PRAN = models.CharField(max_length=255,null=True)
    status=models.CharField(max_length=200,default='Active',null=True)
    isTDS=models.CharField(max_length=200,null=True)
    TDS_percentage = models.IntegerField(null=True,default=0)
    salaryrange = models.CharField(max_length=10, choices=[('1-10', '1-10'), ('10-15', '10-15'), ('15-31', '15-31')], default='1-10',null=True)
    amountperhr = models.IntegerField(default=0,blank=True,null=True)
    workhr = models.IntegerField(default=0,blank=True,null=True)
    uploaded_file=models.FileField(upload_to="images/",null=True)
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    acc_no = models.CharField(null=True,max_length=255)  
    IFSC = models.CharField(max_length=100,null=True)
    bank_name = models.CharField(max_length=100,null=True)
    branch = models.CharField(max_length=100,null=True)
    transaction_type = models.CharField(max_length=100,null=True)

class Holiday(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    holiday_name = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(LoginDetails, on_delete=models.CASCADE, null=True, blank=True)
    company=models.ForeignKey(CompanyDetails, on_delete=models.CASCADE, null=True,blank=True)



class Attendance(models.Model):
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    employee=models.ForeignKey(payroll_employee,on_delete=models.CASCADE,null=True)
    holiday=models.ForeignKey(Holiday,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    status=models.CharField(max_length=255,null=True)
    reason=models.CharField(max_length=255,null=True)

    
class Attendance_History(models.Model):
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    attendance=models.ForeignKey(Attendance,on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    action=models.CharField(max_length=100,null=True)

class Attendance_comment(models.Model):
    company=models.ForeignKey(CompanyDetails,on_delete=models.CASCADE,null=True)
    login_details=models.ForeignKey(LoginDetails,on_delete=models.CASCADE,null=True)
    employee=models.ForeignKey(payroll_employee,on_delete=models.CASCADE,null=True)
    comment = models.TextField(null=True) 
    month = models.IntegerField(null=True)  
    year = models.IntegerField(null=True)  

class Bloodgroup(models.Model):
    Blood_group=models.CharField(max_length=255,null=True)





    
