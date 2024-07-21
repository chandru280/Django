from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    standard = models.CharField(max_length=100)
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



class Testname(models.Model):
    test_name = models.CharField(max_length=100)
    standard = models.CharField(max_length=100)

    def __str__(self):
        return self.test_name

class Testsubject(models.Model):
    test_name = models.ForeignKey(Testname, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    def __str__(self):
        return f"  {self.test_name} in {self.subject}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Testname, on_delete=models.CASCADE)
    subject = models.ForeignKey(Testsubject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.marks}"
    
