from django.db import models
from django.contrib.auth.models import User
import string 
import random 

class Attendee(models.Model):
    YEAR = (('I Year', 'I Year'), ('II Year', 'II Year'), ('III Year', 'III Year'), ('IV Year', 'IV Year'))
    WEB = (('AI - Prediction Machines', 'AI - Prediction Machines'), ('A complete vision to IEEE organisational structure and its benifits', 'A complete vision to IEEE organisational structure and its benifits'), ('Both', 'Both'))
    STUFAC = (('Student', 'Student'), ('Faculty', 'Faculty'))
    name = models.CharField(max_length=100)
    uqno = models.CharField(primary_key=True, max_length=6, unique=True, default=''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)))
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    webinar = models.CharField(max_length=200, choices=WEB)
    dept = models.CharField(max_length=100)
    year = models.CharField(max_length=8, choices=YEAR)
    college = models.CharField(max_length=200)
    stufac = models.CharField(max_length=15, choices=STUFAC)
    desg = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    
class ResourcePerson(models.Model):
    avatar = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Schedules(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Alerts(models.Model):
    COLOR = (('primary', 'Blue'),('success', 'Green'), ('warning', 'Yellow'), ('danger', 'Red'))
    alert = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=10, choices=COLOR)

    class Meta:
        ordering = ['-time_stamp']

    def __str__(self):
        return self.alert

class Feedback(models.Model):
    WEB = (('AI - Prediction Machines', 'AI - Prediction Machines'), ('A complete vision to IEEE organisational structure and its benifits', 'A complete vision to IEEE organisational structure and its benifits'), ('Both', 'Both'))
    user = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    feedback = models.TextField()
    webinar = models.CharField(max_length=200, choices=WEB)

    def __str__(self):
        return self.user.name