from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.core.validators import RegexValidator



class Subject(models.Model):
    # participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_staff':true})
    lecture_name = models.CharField(max_length=200)
    lecture_description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    lecture_date = models.DateTimeField(blank=True, null=True)
    students_number = models.IntegerField()

    def __str__(self):
        # local_t = self.lecture_date.astimezone(Local)
        return '{0} {1}'.format(self.lecture_name, self.lecture_date.strftime("%d/%m/%Y  в %H:%M %z"))

class Student(models.Model):
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'\+7\s?[\(]{0,1}9[0-9]{2}[\)]{0,1}\s?\d{3}[-]{0,1}\d{2}[-]{0,1}\d{2}', message="Введенный номер телефона должен быть в следующем формате: '+7(999)999-99-99'")
    phone_number = phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    def __str__(self):
        name = '{1} {0}'.format(self.participant.first_name, self.participant.last_name)
        if name == ' ':
            name = '{}'.format(self.participant.username)
        return name

class Lecture(models.Model):
    lecture = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_info = models.ForeignKey(Student, on_delete=models.CASCADE)


    def __str__(self):
        return '{0} {1}'.format(self.lecture.lecture_name, self.student_info.participant.username)
