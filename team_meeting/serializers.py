from django.db import transaction
from rest_framework import serializers

from team_meeting.models import (
    MeetingRoom,
    Project,
    TypeOfMeeting,
    Team,
    Meeting,
    Booking
)


class MeetingRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingRoom
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ("name", "description")


class ProjectTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("name", "num_of_members")


class ProjectRetrieveSerializer(ProjectSerializer):
    teams = ProjectTeamSerializer(many=True)

    class Meta:
        model = Project
        fields = ("name", "description", "image", "teams")


class ProjectImageSerializer(ProjectSerializer):

    class Meta:
        model = Project
        fields = ("id", "image")


class TypeOfMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfMeeting
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = "__all__"


class TeamListSerializer(TeamSerializer):
    project = serializers.CharField(
        source="project.name", read_only=True
    )

    class Meta:
        model = Team
        fields = "__all__"


class TeamRetrieveSerializer(TeamSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Team
        fields = "__all__"


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = "__all__"


class MeetingListSerializer(MeetingSerializer):
    team = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )
    project = serializers.CharField(
        source="team.project",
        read_only=True
    )
    type_of_meeting = serializers.CharField()

    class Meta:
        model = Meeting
        fields = (
            "id",
            "team",
            "project",
            "type_of_meeting",
            "requires_meeting_room"
        )


class MeetingCreateSerializer(MeetingSerializer):

    class Meta:
        model = Meeting
        fields = ("team", "type_of_meeting", "requires_meeting_room")


class MeetingRetrieveSerializer(MeetingSerializer):
    team_name = serializers.CharField(source="team.name")
    team_size = serializers.IntegerField(source="team.num_of_members")
    project = ProjectSerializer(source="team.project")
    type_of_meeting = serializers.CharField()

    class Meta:
        model = Meeting
        fields = (
            "id",
            "team_name",
            "team_size",
            "project",
            "type_of_meeting",
            "requires_meeting_room"
        )


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"


class BookingMeetingSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source="team.name")
    project = serializers.CharField(source="team.project.name")
    type_of_meeting = serializers.CharField()

    class Meta:
        model = Meeting
        fields = ("team", "project", "type_of_meeting")


class BookingListSerializer(BookingSerializer):
    time = serializers.CharField(source="duration", read_only=True)
    room = serializers.CharField(source="room.name")
    user = serializers.CharField(source="user.email")
    meeting = BookingMeetingSerializer()

    class Meta:
        model = Booking
        fields = ("id", "day", "time", "room", "user", "meeting")


class BookingRetrieveSerializer(BookingListSerializer):
    room = MeetingRoomSerializer()
    meeting = MeetingListSerializer()


class BookingCreateSerializer(BookingSerializer):
    meeting = MeetingCreateSerializer(read_only=False)

    def create(self, validated_data):
        print(validated_data)
        with transaction.atomic():
            meeting_data = validated_data.pop("meeting")
            meeting = Meeting.objects.create(**meeting_data)
            booking = Booking.objects.create(meeting=meeting, **validated_data)

            return booking
