"""student_info_sis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sims_app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_page, name='dashboard'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('student/', create_student_page, name='student'),
    path('update_student/<str:pk>/', edit_student_page, name='update_student'),
    path('delete_student/<str:pk>/', delete_student_page, name='delete_student'),
    path('student_qualifications/<str:pk>/', qualifications_page, name='student_qualifications'),
    path('course/', create_course_page, name='course'),
    path('update_course/<str:pk>/', edit_course_page, name='update_course'),
    path('delete_course/<str:pk>/', delete_course_page, name='delete_course'),
    path('enroll/', create_enroll_page, name='enroll'),
    path('update_enroll/<str:pk>/', edit_enroll_page, name='update_enroll'),
    path('delete_enroll/<str:pk>/', delete_enroll_page, name='delete_enroll'),
    path('payment/', create_payment_page, name='payment'),
    path('update_payment/<str:pk>/', edit_payment_page, name='update_payment'),
    path('delete_payment/<str:pk>/', delete_payment_page, name='delete_payment'),
    path('exam/', create_exam_page, name='exam'),
    path('update_exam/<str:pk>/', edit_exam_page, name='update_exam'),
    path('delete_exam/<str:pk>/', delete_exam_page, name='delete_exam'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)