from rest_framework import serializers

from team_meeting.models import MeetingRoom


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"
