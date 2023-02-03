from django.db import models

# Create your models here.
class Student(models.Model):
    gender_lookup = (('Male','Male'),('Female','Female'))
    sid = models.CharField(primary_key = True, max_length=10)
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    bdate = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True, choices=gender_lookup)
    mobile = models.CharField(max_length=10, null=True)
    other_phone = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.fname + " " + self.lname

class St_Qualification(models.Model):
    quali_lookup = (('A/L','A/L'),('O/L','O/L'),('HND','HND'),('BSc','BSc'),('MSc','MSc'),('MBA','MBA'),('PHD','PHD'))
    student = models.ForeignKey(Student, null=True, on_delete= models.SET_NULL)
    quali_type = models.CharField(max_length=10, null=True, choices=quali_lookup)
    quali_detail = models.CharField(max_length=100, null=True)

class Course(models.Model):
    ctype_lookup = (('Weekday','Weekday'),('Weekend','Weekend'))
    medium_lookup = (('Sinhala','Sinhala'),('English','English'),('Tamil','Tamil'))
    cid = models.CharField(primary_key = True, max_length=10)
    cname = models.CharField(max_length=50, null=True)
    duration = models.IntegerField(null=True)
    ctype = models.CharField(max_length=10, null=True, choices=ctype_lookup)
    fee = models.IntegerField(null=True)
    medium = models.CharField(max_length=50, null=True, choices=medium_lookup)

    def __str__(self):
        return self.cname

class Enroll(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete= models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete= models.SET_NULL)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

class Payment(models.Model):
    paytype_lookup = (('Downpay','Downpay'),('RegFee','RegFee'),('Installements','Installements'),('CertificateFee','CertificateFee'),('Other','Other'))
    student = models.ForeignKey(Student, null=True, on_delete= models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete= models.SET_NULL)
    pay_date = models.DateField(null=True)
    pay_type = models.CharField(max_length=30, null=True, choices=paytype_lookup)
    pay_note = models.CharField(max_length=80, null=True)
    amount = models.IntegerField(null=True)

class Exam(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete= models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete= models.SET_NULL)
    exam_id = models.CharField(max_length=10, null=True, unique=True)
    module = models.CharField(max_length=25, null=True)
    marks = models.IntegerField(null=True)
    grade = models.CharField(max_length=1, null=True)
    comment = models.CharField(max_length=80, null=True) 

