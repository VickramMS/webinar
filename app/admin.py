from django.contrib import admin
from .models import *

admin.site.register(Attendee)
admin.site.register(ResourcePerson)
admin.site.register(Schedules)
admin.site.register(Alerts)
admin.site.register(Feedback)
admin.site.register(Contact)