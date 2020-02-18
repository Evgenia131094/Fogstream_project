from django.shortcuts import render
from django.utils import timezone
from .models import Subject, Student, Lecture
from qr_code.qrcode.utils import QRCodeOptions
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_exempt

def qr_gen(request):
    
    context = dict(
        my_options=QRCodeOptions(size='t', border=6, error_correction='L'),
    )
    # data = json.loads(request.body.decode('utf-8'))
    data = request.read()
    data = json.loads(data.decode('utf-8'))

    if int(data['count']) > 0:
        Subject.objects.filter(id=data['lectureid']).update(students_number=data['count'])
        


    return render(request, 'fogstream_studying_root/qr_gen.html', {'subjects': "http://{0}/qr_read_view?count={1}&id={2}".format(settings.BASE_URL,data['count'], data['lectureid'])})
    # return render(request, 'fogstream_studying_root/qr_gen.html', context=context)

@csrf_exempt
def reg_on_lecture(request):
    buf = request.read()
    data = json.loads(buf.decode('utf-8'))

    lecture = Subject.objects.get(id=data['lectureid'])
    if Lecture.objects.filter(lecture=lecture).count() < lecture.students_number:

        if data['studentid']!="0":
            student = Student.objects.get( id=data['studentid'])
        else:
            try:
                student = Student.objects.get(phone_number=data['phone'])
            except Student.DoesNotExist:
                student = None
                status = 0
            
        
        if lecture and student:
            if Lecture.objects.filter(lecture=lecture, student_info=student).exists():
                status = 2
            else:
                Lecture(lecture=lecture, student_info=student).save()
                status = 1
    else:
        status = 3

    return render(request, 'fogstream_studying_root/reg_on_lecture.html', {'status': status})

@login_required(login_url='/admin')
def page_view(request):
    subjects = Subject.objects.all().order_by('id')
    return render(request, 'fogstream_studying_root/qr_view.html', {'subjects': subjects})


def qr_read_view(request):
    students = Student.objects.all().order_by('id')
    cur_lecture = Subject.objects.get(id=request.GET.get('id'))
    return render(request, 'fogstream_studying_root/qr_read_view.html', {'students': students, 'lecture': cur_lecture})
