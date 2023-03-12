from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient

from team_meeting.models import MeetingRoom, Project, Team, TypeOfMeeting, Meeting, Booking

BOOKING_URL = reverse("team-meeting:booking-list")
#
#
def sample_room(**params):
    defaults = {
        "name": "Blue",
        "capacity": 20,
    }
    defaults.update(params)

    return MeetingRoom.objects.create(**defaults)


def sample_project(**params):
    defaults = {
        "name": "Taxi",
    }
    defaults.update(params)

    return Project.objects.create(**defaults)


def sample_team(**params):
    project = sample_project()

    defaults = {
        "name": "Backend",
        "project": project,
        "num_of_members": 5,
    }
    defaults.update(params)

    return Team.objects.create(**defaults)


def sample_meeting(**params):
    team = sample_team()
    type_of_meeting = TypeOfMeeting.objects.create("WEEKLY")

    defaults = {
        "team": team,
        "type_of_meeting": type_of_meeting,
        "requires_meeting_room": True,
    }
    defaults.update(params)

    return Meeting.objects.create(**defaults)


def sample_booking(**params):
    room = sample_room()
    meeting = sample_meeting()

    defaults = {
        "room": room,
        "day": "2023-01-01",
        "start_hour": 10,
        "end_hour": 12,
        "user": params["user"],
        "meeting": meeting,
    }
    defaults.update(params)

    return Booking.objects.create(**defaults)


class UnauthenticatedBookingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOKING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
