from django.db import models
from django.conf import settings
# Create your models here.

class Employees(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    Role_CHOICES=[
        ('CEO','CEO'),
        ('Branch Manager','Branch Manager'),
        ('Staff head','Staff head'),
        ('Employee','Employee'),
        ('Accountant',"Accountant"),
        ('Staff','Staff')
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name="employee_account" ) # unique reverse relation
    gender = models.CharField(
    max_length=1,
    choices=GENDER_CHOICES,
    default='M',   # default value
    )
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    temp_address=models.TextField(blank=True,null=True)
    perm_address=models.TextField(blank=True,null=True)
    country=models.CharField(max_length=50,blank=True,null=True)
    zip_code=models.CharField(max_length=10,blank=True,null=True)
    photo=models.ImageField(upload_to='employee_photos/',blank=True,null=True)
    role=models.CharField(max_length=20,choices=Role_CHOICES,default='Employee')
    outlet = models.ForeignKey('outlets.Outlet', on_delete=models.CASCADE, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = "db_employees"
