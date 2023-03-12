from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from team_meeting.models import (
    MeetingRoom,
    Project,
    TypeOfMeeting,
    Team
)
from team_meeting.serializers import (
    MeetingRoomSerializer,
    ProjectSerializer,
    ProjectRetrieveSerializer,
    ProjectImageSerializer,
    TypeOfMeetingSerializer,
    TeamSerializer, TeamListSerializer, TeamRetrieveSerializer
)


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

        if self.action == "create":
            return ProjectSerializer

        if self.action == "upload_image":
            return ProjectImageSerializer

        return ProjectSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific project"""
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TypeOfMeetingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = TypeOfMeeting.objects.all()
    serializer_class = TypeOfMeetingSerializer


class TeamViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer

        if self.action == "retrieve":
            return TeamRetrieveSerializer

        return TeamSerializer
