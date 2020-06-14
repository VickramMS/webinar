from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.views import login_required

def home(request):
    context = {
        "rps1": ResourcePerson.objects.get(id=1),
        "rps2": ResourcePerson.objects.get(id=2),
        "rps3": ResourcePerson.objects.get(id=3),
    }
    return render(request, 'app/home.html', context)

def register(request):
    if request.method == "POST":
        try:
            obj = Attendee.objects.get(email=request.POST.get("email"))
        except:
            obj = None
        if obj != None:
            messages.error(request, 'It seems you have already registered with this email!')
        else:
            attendee = Attendee()
            attendee.name = request.POST.get("name")
            attendee.email = request.POST.get("email")
            attendee.mobile = request.POST.get("mobile")
            attendee.webinar = request.POST.get("webinar")
            attendee.dept = request.POST.get("dept")
            attendee.year = request.POST.get("year")
            attendee.college = request.POST.get("college")
            attendee.desg = request.POST.get("designation")
            attendee.save()
            messages.success(request, "You registration is successfull! Do keep an eye on the webiste's <b>Alerts</b> section for updates!")
    return render(request, 'app/register.html')

@login_required
def dashboard(request):
    context = {
        "objects": Attendee.objects.all(),
        "students": Attendee.objects.filter(desg='Student'),
        "faculty": Attendee.objects.filter(desg='Faculty'),
    }
    return render(request, 'app/dashboard.html', context)

@login_required
def report(request):
    context = {
        "objects": Attendee.objects.all(),
        "aiobj": list(Attendee.objects.filter(webinar="AI in Human Health")) + list(Attendee.objects.filter(webinar="Both")),
        "ieeeobj": list(Attendee.objects.filter(webinar="Importance of IEEE")) + list(Attendee.objects.filter(webinar="Both"))
    }

    return render(request, 'app/report.html', context)

def alerts(request):
    context = {
        "schedules": Schedules.objects.all(),
        "alerts": Alerts.objects.all()
    }
    return render(request, 'app/alert.html', context)

def newlink(request):
    if request.method == "POST":
        schedules = Schedules()
        schedules.name = request.POST.get("name")
        schedules.link = request.POST.get("link")
        schedules.save()
        messages.success(request, 'New Link has been posted successfully')
        return redirect('alerts')
    return render(request, 'app/alert.html')
    
def editschedules(request):
    context = {
        "schedules": Schedules.objects.all(),
    }
    if request.method == "POST":
        count = request.POST.get("count")
        for i in range(1, (int(count)+1)):
            schedule = Schedules.objects.get(id=request.POST.get("id-"+ str(i)))
            schedule.name = request.POST.get("val-"+ str(i))
            schedule.link = request.POST.get("link-"+ str(i))
            schedule.save()
        messages.success(request, 'Links has been Updated')
        return redirect('alerts')

    return render(request, 'app/edit_Schedules.html', context)

def newalert(request):
    if request.method  == "POST":
        alerts = Alerts()
        alerts.alert = request.POST.get("new-alert")
        alerts.color = request.POST.get("new-color")
        alerts.save()
        messages.success(request, 'New Alert has been posted successfully!')
        return redirect('alerts')
    return render(request, 'app/alerts.html')

def alertsedit(request):
    context = {
        "alerts": Alerts.objects.all(),
    }
    if request.method == "POST":
        count = int(request.POST.get("count"))
        for i in range(1, (count+1)):
            alert = Alerts.objects.get(id=request.POST.get("id-"+str(i)))
            alert.alert = request.POST.get("alert-"+str(i))
            alert.color = request.POST.get("color-"+str(i))
            alert.save()
        messages.success(request, 'Alerts have been updated')
        return redirect('alerts')
    return render(request, 'app/alerts.html', context)