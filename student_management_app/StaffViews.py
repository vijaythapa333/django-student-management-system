from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, Attendance, AttendanceReport


def staff_home(request):
    context={

    }
    return render(request, "staff_template/staff_home_template.html", context)



def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/take_attendance_template.html", context)





# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in students:
        data_small={"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)




@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
        attendance.save()

        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")

