from django.contrib import admin

from .models import (
    MeetingRoom,
    Project,
    Team,
    TypeOfMeeting,
    Meeting,
    Booking,
)

admin.site.register(MeetingRoom)
admin.site.register(Project)
admin.site.register(Team)
admin.site.register(TypeOfMeeting)
admin.site.register(Meeting)
admin.site.register(Booking)
