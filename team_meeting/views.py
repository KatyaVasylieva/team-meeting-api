from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from team_meeting.models import MeetingRoom, Project
from team_meeting.serializers import MeetingRoomSerializer, ProjectSerializer, ProjectRetrieveSerializer


class MeetingRoomViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    # permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectSerializer

        if self.action == "retrieve":
            return ProjectRetrieveSerializer

        return ProjectSerializer
