from rest_framework import serializers

from team_meeting.models import MeetingRoom, Project, TypeOfMeeting, Team


class MeetingRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingRoom
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ("name", "description")


class ProjectRetrieveSerializer(ProjectSerializer):

    class Meta:
        model = Project
        fields = ("name", "description", "image")


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
