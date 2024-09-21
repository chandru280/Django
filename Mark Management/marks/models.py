from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = [
    ('ADMIN', 'Admin'),
    ('STAFF', 'Staff'),
    ('STUDENT', 'Student'),
]

class UserForm(AbstractUser):
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    id = models.IntegerField(primary_key=True)
    text =  models.CharField(max_length=50, null=True, blank=True)
    contact = models.IntegerField(default=0, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile')
    

      
    # Permission fields
    can_add = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']




class Standard(models.Model):
    standard = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.standard

class Subject(models.Model):
    name = models.CharField(max_length=100)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Student(models.Model):
    name = models.CharField(max_length=100)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    guardian_name = models.CharField(max_length=100)
    guardian_contact = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    blood_group = models.CharField(max_length=5)
    admission_number = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    admission_date = models.DateField()
    previous_school = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    contact_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20)
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)

    def __str__(self):
        return self.name




class Testname(models.Model):
    test_name = models.CharField(max_length=100)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.test_name

class Testsubject(models.Model):
    test_name = models.ForeignKey(Testname, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_mark = models.IntegerField(null=True, blank=True)
    pass_mark = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.test_name} in {self.subject}"



class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Testname, on_delete=models.CASCADE)
    subject = models.ForeignKey(Testsubject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], null=True)

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.marks}"
    



