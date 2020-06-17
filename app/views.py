from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.views import login_required
import string 
import random 

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
            attendee.stufac = request.POST.get("stufac")
            attendee.desg = request.POST.get("desg")
            attendee.uqno = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
            attendee.save()
            messages.success(request, "You registration is successfull! Do keep an eye on the webiste's <b>Alerts</b> section for updates!")
    return render(request, 'app/register.html')

@login_required
def dashboard(request):
    context = {
        "objects": Attendee.objects.all(),
        "students": Attendee.objects.filter(stufac='Student'),
        "faculty": Attendee.objects.filter(stufac='Faculty'),
    }
    return render(request, 'app/dashboard.html', context)

@login_required
def report(request):
    context = {
        "objects": Attendee.objects.all(),
        "aiobj": list(Attendee.objects.filter(webinar="AI - Prediction Machines")) + list(Attendee.objects.filter(webinar="Both")),
        "ieeeobj": list(Attendee.objects.filter(webinar="A complete vision to IEEE organisational structure and its benifits")) + list(Attendee.objects.filter(webinar="Both"))
    }

    return render(request, 'app/report.html', context)

def alerts(request):
    context = {
        "alerts": Alerts.objects.all()
    }
    if request.method == "POST":
        try:
            user = Attendee.objects.get(email=request.POST.get("email"))
            return redirect('links', pk=user.uqno)
        except:
            messages.warning(request, 'The entered Email is not registered.')
    return render(request, 'app/alert.html', context)


def links(request, pk):
    context = {
        "schedules": Schedules.objects.all(),
    }
    return render(request, 'app/links.html', context)

def newlink(request):
    if request.method == "POST":
        schedules = Schedules()
        schedules.name = request.POST.get("name")
        schedules.link = request.POST.get("link")
        schedules.save()
        messages.success(request, 'New Link has been posted successfully')
        return redirect('alerts')
    return render(request, 'app/alert.html')

@login_required
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

    return render(request, 'app/edit_schedules.html', context)

@login_required
def newalert(request):
    if request.method  == "POST":
        alerts = Alerts()
        alerts.alert = request.POST.get("new-alert")
        alerts.color = request.POST.get("new-color")
        alerts.save()
        messages.success(request, 'New Alert has been posted successfully!')
        return redirect('alerts')
    return render(request, 'app/alerts.html')

@login_required
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


def feedback(request):
    if request.method  == "POST":
        try:
            user = Attendee.objects.get(email=request.POST.get("email"))
            webinar = request.POST.get("webinar")
            try:
                length = len(list(Feedback.objects.filter(webinar=webinar, user=user)))
                if length == 0:
                    if user.webinar == webinar or user.webinar == "Both":
                        feedback = Feedback()
                        feedback.user = user
                        feedback.webinar = webinar
                        feedback.qs1 = request.POST.get("qs-1")
                        feedback.qs2 = request.POST.get("qs-2")
                        feedback.qs3 = request.POST.get("qs-3")
                        feedback.qs4 = request.POST.get("qs-4")
                        feedback.qs5 = request.POST.get("qs-5")
                        feedback.qs6 = request.POST.get("qs-6")
                        feedback.feedback = request.POST.get("feedback")
                        feedback.save()
                        messages.success(request, 'Your feedback has been submited')
                        return redirect('alerts')
                    else:
                        messages.warning(request, 'You cannot give a feedback to a session which you have not enrolled')
                else:
                    messages.warning(request, 'You have already given your feedback')
            except:
                pass
        except:
            messages.warning(request, 'It seems you have entered an email id that has not been registered. Please contact the support.')
    return render(request, 'app/feedback.html')

@login_required
def feedbackview(request):
    context = {
        "feedback": Feedback.objects.filter(webinar='AI - Prediction Machines'),
        "qs1": Feedback.objects.values_list('qs1', flat=True).filter(webinar='AI - Prediction Machines'),
        "qs2": Feedback.objects.values_list('qs2', flat=True).filter(webinar='AI - Prediction Machines'),
        "qs3": Feedback.objects.values_list('qs3', flat=True).filter(webinar='AI - Prediction Machines'),
        "qs4": Feedback.objects.values_list('qs4', flat=True).filter(webinar='AI - Prediction Machines'),
        "qs5": Feedback.objects.values_list('qs5', flat=True).filter(webinar='AI - Prediction Machines'),
        "qs6": Feedback.objects.values_list('qs6', flat=True).filter(webinar='AI - Prediction Machines'),
        "feedback1": Feedback.objects.filter(webinar='A complete vision to IEEE organisational structure and its benifits'),
        "qs11": Feedback.objects.values_list('qs1', flat=True).filter(webinar='A complete vision to IEEE organisational structure and its benifits'),
        "qs21": Feedback.objects.values_list('qs2', flat=True).filter(webinar='A complete vision to IEEE organisational structure and its benifits'),
        "qs31": Feedback.objects.values_list('qs3', flat=True).filter(webinar='A complete vision to IEEE organisational structure and its benifits'),
        "qs41": Feedback.objects.values_list('qs4', flat=True).filter(webinar='A complete vision to IEEE organisational structure and its benifits'),
        "qs51": Feedback.objects.values_list('qs5', flat=True).filter(webinar='A complete vision to IEEE organisational structure and its benifits'),
        "qs61": Feedback.objects.values_list('qs6', flat=True).filter(webinar='A complete vision to IEEE organisational structure and its benifits'),

    }
    return render(request, 'app/feedback_view.html', context)

def validate(request):
    if request.method == "POST":
        email = request.POST.get("email")
        webinar = request.POST.get("webinar")
        try:
            user = Attendee.objects.get(email=email)
            try:
                feedback = Feedback.objects.get(webinar=webinar, user=user)
                if feedback.webinar == 'AI - Prediction Machines':
                    return redirect("certificate", id=user.uqno, pk='ry6qw2')
                elif feedback.webinar == 'A complete vision to IEEE organisational structure and its benifits':
                    return redirect("certificate", id=user.uqno, pk='v6weg3')
                else:
                    messages.warning(request, 'There was a problem while trying to fetch your certificate. Please contact the support')
            except:
                messages.warning(request, 'You have not provided any feedback. Please give a feedback and try again. You can contact the support if you face any issues.')
        except:
            messages.error(request, 'It seems you have not registered with this email. Please check the email. You can contact the support if you face any issues.')
    return render(request, 'app/validate.html')

def certificate(request, id, pk):
    user = Attendee.objects.get(uqno=id)

    context = {
        "attendee": user,
        "certificate": pk,
    }
    return render(request, 'app/certificate.html', context)

def contact(request):
    if request.method == "POST":
        contact = Contact()
        contact.email = request.POST.get("email")
        contact.quiry = request.POST.get("quiry")
        contact.save()
        messages.warning(request, 'Your request has been submitted. We will contact you shortly by email.')
        return redirect("alerts")
    return render(request, 'app/contact.html')