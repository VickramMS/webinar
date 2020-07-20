from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.views import login_required
import string 
import random 
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.views.generic import View
from django.template.loader import get_template 
from sample_project.utils import certificate, report
from django.template import loader


def home(request):
    rps = ResourcePerson.objects.first()
    context = {
        "rps": rps
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
            attendee.gender = request.POST.get("gender")
            attendee.uqno = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
            attendee.save()
            content = {
                "name": attendee.name,
                "dept": attendee.dept,
                "year": attendee.year,
                "college": attendee.college,
                "dept": attendee.dept,
                "desg": attendee.desg,
                "stufac": attendee.stufac,
            }
            html_message = loader.render_to_string('email/confirmation.html', content)
            send_mail(
                subject="GCE BODI - WEBINAR",
                message="This is a confirmation mail from GCE BODI - Webinars. Please find more details in gcebodi.herokuapp.com/alerts/. Thank you!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[str(attendee.email)],
                html_message=html_message,
                fail_silently=False
            )
            messages.success(request, "Please check your <b>email</b> for further updates!")
    return render(request, 'app/register.html')

@login_required
def dashboard(request):
    context = {
        "objects": Attendee.objects.all(),
        "students": Attendee.objects.filter(stufac='Student'),
        "faculty": Attendee.objects.filter(stufac='Faculty'),
        "expert": Attendee.objects.filter(stufac='Industry Expert')
    }
    return render(request, 'app/dashboard.html', context)


def alerts(request):
    context = {
        "alerts": Alerts.objects.all(),
        "schedules": Schedules.objects.all(),
    }
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
                    html_message = loader.render_to_string('email/cert.html', {"obj": user})
                    send_mail(
                        'Certificate - GCE Bodi',
                        'Link to your certificate',
                        settings.EMAIL_HOST_USER,
                        [str(user.email)],
                        fail_silently=False,
                        html_message=html_message
                    )
                    messages.success(request, 'Your feedback has been submited')
                    return redirect('alerts')
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
        "feedback": Feedback.objects.filter(webinar='5G Technology Uses and UE Hazards'),
        "qs1": Feedback.objects.values_list('qs1', flat=True).filter(webinar='5G Technology Uses and UE Hazards'),
        "qs2": Feedback.objects.values_list('qs2', flat=True).filter(webinar='5G Technology Uses and UE Hazards'),
        "qs3": Feedback.objects.values_list('qs3', flat=True).filter(webinar='5G Technology Uses and UE Hazards'),
        "qs4": Feedback.objects.values_list('qs4', flat=True).filter(webinar='5G Technology Uses and UE Hazards'),
        "qs5": Feedback.objects.values_list('qs5', flat=True).filter(webinar='5G Technology Uses and UE Hazards'),
        "qs6": Feedback.objects.values_list('qs6', flat=True).filter(webinar='5G Technology Uses and UE Hazards'),
    }
    return render(request, 'app/feedback_view.html', context)

def contact(request):
    if request.method == "POST":
        contact = Contact()
        contact.email = request.POST.get("email")
        contact.quiry = request.POST.get("quiry")
        contact.save()
        messages.warning(request, 'Your request has been submitted. We will contact you shortly by email.')
        return redirect("alerts")
    return render(request, 'app/contact.html')

def email(request):
    context = {
        "objs": Feedback.objects.all()
    }
    return render(request, 'app/email.html', context)

def delete(request, pk):
    contact = Contact.objects.get(id=pk)
    contact.delete()
    return redirect("email")

def overall(request):
    context = {
        "attendees": Attendee.objects.all()
    }
    return render(request, 'app/overall.html', context)



class GenerateCertificate(View):
    def get(self, request, pk, *args, **kwargs):
        template = get_template('app/certificate.html')
        obj = Attendee.objects.get(uqno=pk)
        context = {
            "obj": Attendee.objects.get(uqno=pk)
        }
        html = template.render(context)
        pdf = certificate('certificate.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = obj.name + ".pdf"
            content = "inline; filename=%s.pdf" %(obj.name)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s.pdf" %(obj.name)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    
class GenerateReport(View):
    def get(self, request, *args, **kwargs):
        template = get_template('app/report.html')
        context = {
            "objects": Attendee.objects.all()
        }
        html = template.render(context)
        pdf = report('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Report.pdf"
            content = "inline; filename=Report"
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=Report"
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def masssendlink(request, pk):
    obj = Schedules.objects.get(id=pk)
    data = []
    for attendee in Attendee.objects.all():
        data.append((
            'GCE BODI - Webinar',
            'Hi %s,\nGreetings from the Institute Industry Interaction Cell, Government College of Engineering, Bodinayakkanur. We are so glad that you have registered for the webinar on 5G Technology and UE Hazards. Here are the details of the webinars that you have enrolled.\n\n5G Technology and UE Hazards | 20th July, 2020 10.00 IST\n      On Microsoft Teams\n            - App must be installed for mobile. (https://play.google.com/store/apps/details?id=com.microsoft.teams&hl=en_IN).\n            - Desktops don’t need application to be installed.\n            - Join the session using the below link.\n                    I.For Desktop users\n                         1.Click the link\n                         2.Choose Continue in this browser\n                         3.Allow Camera and Microphone\n                         4.Enter you Name and keep your camera and mic muted\n                         5.Click Join now\n                    II.For Mobile users (App must be installed)\n                         1.Click the link\n                         2.Click Join as a guest\n                         3.Enter your name\n                         4.Click Join\n            - Link to the session will also be available in the gcebodi.herokuapp.com/alerts page.\n            - Participants are advised to join the session earlier around 9.45am IST.\n\nLink to the Meeting  :  %s\n\nWarm Regards,\nOrganizing Team,\nInsitution Industry Interactive Cell,\nGovernment College of Engineering,\nBodinayakanur - 625582\n' %(attendee.name, obj.link),
            settings.EMAIL_HOST_USER,
            [str(attendee.email)],
        ))
    send_mass_mail(
        tuple(data),
        fail_silently=False
    )
    messages.success(request, 'Mass mail has been sent successfully!')
    return redirect('alerts')
    