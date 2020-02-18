from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime



class Subject(models.Model):
    # participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lecture_name = models.CharField(max_length=200)
    lecture_description = models.TextField()
    created_date = models.DateTimeField(default="Asia/Vladivostok")
    lecture_date = models.DateTimeField(blank=True, null=True)
    students_number = models.IntegerField()

    def __str__(self):
        # local_t = self.lecture_date.astimezone(Local)
        return '{0} {1}'.format(self.lecture_name, self.lecture_date.strftime("%d/%m/%Y  в %H:%M"))

class Student(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return '{1} {0}'.format(self.participant.first_name, self.participant.last_name)

class Lecture(models.Model):
    lecture = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_info = models.ForeignKey(Student, on_delete=models.CASCADE)


    def __str__(self):
        return '{0} {1}'.format(self.lecture.lecture_name, self.student_info.participant.username)