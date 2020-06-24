from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse

from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students


def staff_home(request):
    context={

    }
    return render(request, "staff_template/staff_home_template.html", context)