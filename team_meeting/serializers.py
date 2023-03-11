from rest_framework import serializers

from team_meeting.models import MeetingRoom, Project


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
