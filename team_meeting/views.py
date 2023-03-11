from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from team_meeting.models import MeetingRoom
from team_meeting.serializers import MeetingRoomSerializer


class MeetingRoomViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    # permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
