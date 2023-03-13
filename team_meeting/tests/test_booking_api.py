from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient

from team_meeting.models import MeetingRoom, Project, Team, TypeOfMeeting, Meeting, Booking
from team_meeting.serializers import BookingListSerializer, BookingRetrieveSerializer

BOOKING_URL = reverse("team-meeting:booking-list")


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


def sample_team(project, **params):
    defaults = {
        "name": "Backend",
        "project": project,
        "num_of_members": 5,
    }
    defaults.update(params)

    return Team.objects.create(**defaults)


def sample_meeting(team, type_of_meeting, **params):
    defaults = {
        "team": team,
        "type_of_meeting": type_of_meeting,
        "requires_meeting_room": True,
    }
    defaults.update(params)

    return Meeting.objects.create(**defaults)


def sample_booking(room, meeting, user, **params):
    defaults = {
        "room": room,
        "day": "2023-01-01",
        "start_hour": 10,
        "end_hour": 12,
        "user": user,
        "meeting": meeting,
    }
    defaults.update(params)

    return Booking.objects.create(**defaults)


def detail_url(booking_id):
    return reverse("team-meeting:booking-detail", args=[booking_id])


class UnauthenticatedBookingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOKING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

        self.room_blue = sample_room()
        self.room_yellow = sample_room(name="Yellow")

        self.project_taxi = sample_project()
        self.project_library = sample_project(name="Library")

        self.team_taxi_back = sample_team(self.project_taxi)
        self.team_library_back = sample_team(self.project_library)

        self.weekly_type = TypeOfMeeting.objects.create(name="Weekly")
        self.urgent_type = TypeOfMeeting.objects.create(name="Urgent")

        self.meeting_weekly = sample_meeting(self.team_taxi_back, self.weekly_type)
        self.meeting_urgent = sample_meeting(self.team_library_back, self.urgent_type)

        self.booking_weekly = sample_booking(self.room_blue, self.meeting_weekly, self.user)
        self.booking_urgent = sample_booking(self.room_yellow, self.meeting_urgent, self.user, day="2023-01-02")

    def test_list_bookings(self):

        res = self.client.get(BOOKING_URL)

        bookings = Booking.objects.order_by("day", "start_hour")
        serializer = BookingListSerializer(bookings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_bookings_by_day(self):

        res = self.client.get(
            BOOKING_URL, {"day": "2023-01-02"}
        )

        serializer_w = BookingListSerializer(self.booking_weekly)
        serializer_u = BookingListSerializer(self.booking_urgent)

        self.assertIn(serializer_u.data, res.data)
        self.assertNotIn(serializer_w.data, res.data)

    def test_filter_bookings_by_room(self):

        res = self.client.get(
            BOOKING_URL, {"room": "b"}
        )

        serializer_w = BookingListSerializer(self.booking_weekly)
        serializer_u = BookingListSerializer(self.booking_urgent)

        self.assertIn(serializer_w.data, res.data)
        self.assertNotIn(serializer_u.data, res.data)

    def test_filter_bookings_by_project(self):

        res = self.client.get(
            BOOKING_URL, {"project": "lib"}
        )

        serializer_w = BookingListSerializer(self.booking_weekly)
        serializer_u = BookingListSerializer(self.booking_urgent)

        self.assertIn(serializer_u.data, res.data)
        self.assertNotIn(serializer_w.data, res.data)

    def test_retrieve_booking_detail(self):
        url = detail_url(self.booking_weekly.id)
        res = self.client.get(url)

        serializer = BookingRetrieveSerializer(self.booking_weekly)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_booking_with_correct_data(self):
        payload = {
            "room": 1,
            "day": "2023-01-03",
            "start_hour": 10,
            "end_hour": 12,
            "user": 1,
            "meeting": {
                "team": 1,
                "type_of_meeting": 1,
            }
        }
        res = self.client.post(BOOKING_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.last()

        for key in ["start_hour", "end_hour"]:
            self.assertEqual(payload[key], getattr(booking, key))
        self.assertEqual(self.room_blue, getattr(booking, "room"))
        self.assertEqual("2023-01-03", str(getattr(booking, "day")))
        self.assertEqual(self.user, getattr(booking, "user"))
        self.assertEqual(Meeting.objects.last(), getattr(booking, "meeting"))

    def test_create_booking_with_already_taken_time(self):
        payload = {
            "room": 2,
            "day": "2023-01-02",
            "start_hour": 11,
            "end_hour": 12,
            "user": 1,
            "meeting": {
                "team": 1,
                "type_of_meeting": 1,
            }
        }
        res = self.client.post(BOOKING_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
