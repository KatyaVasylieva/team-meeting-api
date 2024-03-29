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
        fields = "__all__"


class ProjectTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "name", "num_of_members")


class ProjectCreateSerializer(ProjectSerializer):

    class Meta:
        model = Project
        fields = ("name", "description")


class ProjectRetrieveSerializer(ProjectSerializer):
    teams = ProjectTeamSerializer(many=True)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "image", "teams")


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
    project = ProjectRetrieveSerializer()

    class Meta:
        model = Team
        fields = "__all__"


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = "__all__"


class MeetingListSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )
    project = serializers.CharField(
        source="team.project.name",
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


class MeetingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ("team", "type_of_meeting")


class MeetingRetrieveSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source="team.name")
    project = ProjectRetrieveSerializer(source="team.project")
    type_of_meeting = serializers.CharField()

    class Meta:
        model = Meeting
        fields = (
            "id",
            "type_of_meeting",
            "team",
            "project",
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

    class Meta:
        model = Booking
        fields = ("room", "day", "start_hour", "end_hour", "meeting")

    def create(self, validated_data):
        with transaction.atomic():
            meeting_data = validated_data.pop("meeting")
            meeting = Meeting.objects.create(
                requires_meeting_room="True", **meeting_data
            )
            booking = Booking.objects.create(meeting=meeting, **validated_data)
            return booking


class BookingUpdateSerializer(BookingSerializer):

    class Meta:
        model = Booking
        fields = ("room", "day", "start_hour", "end_hour")

    def update(self, instance, validated_data):

        instance.room = validated_data.get("room", instance.room)
        instance.day = validated_data.get("day", instance.day)
        instance.start_hour = validated_data.get(
            "start_hour", instance.start_hour
        )
        instance.end_hour = validated_data.get("end_hour", instance.end_hour)
        instance.save()

        return instance
