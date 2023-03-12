from rest_framework import serializers

from team_meeting.models import MeetingRoom, Project, TypeOfMeeting, Team, Meeting


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

    class Meta:
        model = Meeting
        fields = ("team", "project", "type_of_meeting", "requires_meeting_room")


class MeetingCreateSerializer(MeetingSerializer):

    class Meta:
        model = Meeting
        fields = ("team", "type_of_meeting", "requires_meeting_room")
