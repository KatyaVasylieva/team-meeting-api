from django.urls import path, include
from rest_framework import routers

from team_meeting.views import (
    MeetingRoomViewSet,
)

router = routers.DefaultRouter()
router.register("meeting_rooms", MeetingRoomViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "team-meeting"
