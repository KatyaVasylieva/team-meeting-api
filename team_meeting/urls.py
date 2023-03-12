from django.urls import path, include
from rest_framework import routers

from team_meeting.views import (
    MeetingRoomViewSet,
    ProjectViewSet, TypeOfMeetingViewSet, TeamViewSet,
)

router = routers.DefaultRouter()
router.register("meeting_rooms", MeetingRoomViewSet)
router.register("projects", ProjectViewSet)
router.register("types_of_meeting", TypeOfMeetingViewSet)
router.register("teams", TeamViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "team-meeting"
