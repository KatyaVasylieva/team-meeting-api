from django.urls import path, include
from rest_framework import routers

from team_meeting.views import (
    MeetingRoomViewSet,
    ProjectViewSet,
)

router = routers.DefaultRouter()
router.register("meeting_rooms", MeetingRoomViewSet)
router.register("projects", ProjectViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "team-meeting"
