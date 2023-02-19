from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum, Count
from .forms import *
from .models import *
from .filters import StudentFilter
from .decoraters import unathenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.forms import inlineformset_factory


# Create your views here.


def register_page(request):
        form = CreateUserForm()
    
        if request.method == "POST":
            form = CreateUserForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form':form}
        return render(request,'sims_app/register.html',context)

@unathenticated_user
def login_page(request):

    if request.method == "POST":
        usn = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=usn, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Username or Password is incorrect! ")
    return render(request,'sims_app/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard_page(request):
    enroll_data = Enroll.objects.all()
    registrations_count = enroll_data.count()
    this_month = timezone.now().month
    registrations_this_month = enroll_data.filter(start_date__month = this_month).count

    payment_data = Payment.objects.all()
    payments_total = payment_data.aggregate(Sum('amount'))['amount__sum'] 
    payments_this_month = payment_data.filter(pay_date__month = this_month).aggregate(Sum('amount'))['amount__sum'] 

    student_data = Student.objects.all()
    student_count = student_data.count()
    male_count = student_data.filter(gender='Male').count()
    female_count = student_data.filter(gender='Female').count()

    course_data = Course.objects.all()
    course_count = course_data.count()

    top_courses = payment_data.values('course__cname').annotate(total = Sum('amount')).order_by('-total')[:5]
    top_students = payment_data.values('student__fname','student__lname').annotate(total = Sum('amount')).order_by('-total')[:5]

    exam_data = Exam.objects.all()
    students_performance = exam_data.values('student__profile_pic','student__fname','student__lname').annotate(total = Sum('marks')).order_by('-total').annotate(exam_count =Count('exam_id'))
    best_performer = students_performance[0] 

    context = {'student_count':  student_count, 'female_count':female_count, 'male_count':male_count, 
    'reg_count':registrations_count, 'reg_count_month':registrations_this_month,
    'payments_month':payments_this_month, 'payments_total':payments_total, 'course_count':course_count,
    'top_courses':top_courses, 'top_students':top_students, 'students_performance':students_performance,
    'best_performer':best_performer,
    }

    return render(request,'sims_app/dashboard.html', context)


def create_student_page(request):
    student_records = Student.objects.all()

    student_filter = StudentFilter(request.GET, queryset=student_records)
    student_records= student_filter.qs

    form = CreateStudentForm()
    if request.method == "POST":
        form = CreateStudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student')
            
    context = {'form':form, 'student_records':student_records, 'student_filter':student_filter}
    return render(request,'sims_app/student.html',context)


def edit_student_page(request, pk):
    student_instance = Student.objects.get(sid=pk)
    
    form = CreateStudentForm(instance=student_instance) 
    if request.method == "POST":
        form = CreateStudentForm(request.POST, request.FILES, instance=student_instance)
        if form.is_valid():
            form.save()
            return redirect('student')
    context = {'form':form}
    return render(request,'sims_app/edit_student.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_student_page(request, pk):
    student_instance = Student.objects.get(sid=pk)
    if request.method == "POST":
        student_instance.delete()
        return redirect('student')
    context = {'item':student_instance}
    return render(request,'sims_app/delete_student.html',context)

def qualifications_page(request, pk):
    QualificationFormSet = inlineformset_factory(Student, St_Qualification, fields=('quali_type','quali_detail'), extra=1)
    student_instance = Student.objects.get(sid=pk)
    formset = QualificationFormSet(instance=student_instance)
    if request.method == "POST":
        formset = QualificationFormSet(request.POST,instance=student_instance)
        if formset.is_valid():
            formset.save()
            return redirect('student')
    context = {'formset':formset, 'student':student_instance}
    return render(request,'sims_app/qualification_form.html',context)


def delete_qualifications_page(request, pk):
    QualificationFormSet = inlineformset_factory(Student, St_Qualification, fields=('quali_type','quali_detail'), extra=1, can_delete=True)
    student_instance = Student.objects.get(sid=pk)
    formset = QualificationFormSet(instance=student_instance)
    if request.method == "POST":
      if "delete-qualifications" in request.POST:
        
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data.get("DELETE"):
                        qualification = form.instance
                        qualification.delete()
                        return redirect("student_qualifications")
    context = {'formset':formset }
    return render(request,'sims_app/delete_qualification.html',context)

""" def qualifications_page(request, pk):
    QualificationFormSet = inlineformset_factory(Student, St_Qualification, fields=('quali_type','quali_detail'), extra=1, can_delete=True)
    student_instance = Student.objects.get(sid=pk)
    formset = QualificationFormSet(instance=student_instance)
    if request.method == "POST":
        formset = QualificationFormSet(request.POST,instance=student_instance)
        if "confirm" in request.POST:
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data.get("DELETE"):
                        qualification = form.instance
                        qualification.delete()
                return redirect("student_qualifications")
        elif formset.is_valid():
            formset.save()
            return redirect('student')
    context = {'formset':formset, 'student':student_instance}
    return render(request,'sims_app/qualification_form.html',context) """


def create_course_page(request):
    course_records = Course.objects.all()
    form = CreateCourseForm()
    if request.method == "POST":
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course')
            
    context = {'form':form, 'course_records':course_records}
    return render(request,'sims_app/course.html',context)


def edit_course_page(request, pk):
    course_records = Course.objects.get(cid=pk)
    
    form = CreateCourseForm(instance=course_records) 
    if request.method == "POST":
        form = CreateCourseForm(request.POST, instance=course_records)
        if form.is_valid():
            form.save()
            return redirect('course')
    context = {'form':form}
    return render(request,'sims_app/edit_course.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_course_page(request, pk):
    course_instance = Course.objects.get(cid=pk)
    if request.method == "POST":
        course_instance.delete()
        return redirect('course')
    context = {'item':course_instance}
    return render(request,'sims_app/delete_course.html',context)


def create_enroll_page(request):
    enroll_records = Enroll.objects.all()
    form = CreateEnrollForm()
    if request.method == "POST":
        form = CreateEnrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll')
            
    context = {'form':form, 'enroll_records':enroll_records}
    return render(request,'sims_app/enroll.html',context)


def edit_enroll_page(request, pk):
   enroll_records = Enroll.objects.get(id=pk)
   form = CreateEnrollForm(instance=enroll_records)
   if request.method == "POST":
    form = CreateEnrollForm(request.POST, instance=enroll_records)
    if form.is_valid():
        form.save()
        return redirect('enroll')
   context = {'form':form, 'enroll_records':enroll_records}
   return render(request,'sims_app/edit_enroll.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_enroll_page(request, pk):
    enroll_records = Enroll.objects.get(id=pk)
    if request.method == "POST":
        enroll_records.delete()
        return redirect('enroll')
    context = {'item':enroll_records}
    return render(request,'sims_app/delete_enroll.html',context)


def create_payment_page(request):
    payment_records = Payment.objects.all()
    form = CreatePaymentForm()
    if request.method == "POST":
        form = CreatePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment')
            
    context = {'form':form, 'payment_records':payment_records}
    return render(request,'sims_app/payment.html',context)


def edit_payment_page(request, pk):
   payment_records = Payment.objects.get(id=pk)
   form = CreatePaymentForm(instance=payment_records)
   if request.method == "POST":
    form = CreatePaymentForm(request.POST, instance=payment_records)
    if form.is_valid():
        form.save()
        return redirect('payment')
   context = {'form':form, 'payment_records':payment_records}
   return render(request,'sims_app/edit_payment.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_payment_page(request, pk):
    payment_records = Payment.objects.get(id=pk)
    if request.method == "POST":
        payment_records.delete()
        return redirect('payment')
    context = {'item':payment_records}
    return render(request,'sims_app/delete_payment.html',context)


def create_exam_page(request):
    exam_records = Exam.objects.all()
    form = CreateExamForm()
    if request.method == "POST":
        form = CreateExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam')
            
    context = {'form':form, 'exam_records':exam_records}
    return render(request,'sims_app/exam.html',context)


def edit_exam_page(request, pk):
   exam_records = Exam.objects.get(id=pk)
   form = CreateExamForm(instance=exam_records)
   if request.method == "POST":
    form = CreateExamForm(request.POST, instance=exam_records)
    if form.is_valid():
        form.save()
        return redirect('exam')
   context = {'form':form, 'exam_records':exam_records}
   return render(request,'sims_app/edit_exam.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_exam_page(request, pk):
    exam_records = Exam.objects.get(id=pk)
    if request.method == "POST":
        exam_records.delete()
        return redirect('exam')
    context = {'item':exam_records}
    return render(request,'sims_app/delete_exam.html',context)

@allowed_users(allowed_roles=['admin'])
def user_dashboard_page(request):
    users_data = Profile.objects.all().values('profile_pic','user__username','user__email')
   
    form = CreateUserForm()
    if request.method == "POST":
            form = CreateUserForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('users')
    context = {'form':form,'users_data':users_data}
    return render(request,'sims_app/users.html',context)
