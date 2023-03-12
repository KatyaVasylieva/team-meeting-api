from datetime import datetime

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from team_meeting.models import (
    MeetingRoom,
    Project,
    TypeOfMeeting,
    Team, Meeting, Booking
)
from team_meeting.serializers import (
    MeetingRoomSerializer,
    ProjectSerializer,
    ProjectRetrieveSerializer,
    ProjectImageSerializer,
    TypeOfMeetingSerializer,
    TeamSerializer,
    TeamListSerializer,
    TeamRetrieveSerializer,
    MeetingSerializer,
    MeetingListSerializer,
    MeetingCreateSerializer,
    MeetingRetrieveSerializer,
    BookingSerializer,
    BookingListSerializer,
    BookingRetrieveSerializer,
    BookingCreateSerializer
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

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

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

    def get_queryset(self):
        name = self.request.query_params.get("name")
        project = self.request.query_params.get("project")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        if project:
            queryset = queryset.filter(project__name__icontains=project)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TeamListSerializer

        if self.action == "retrieve":
            return TeamRetrieveSerializer

        return TeamSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get_queryset(self):
        project = self.request.query_params.get("project")

        queryset = self.queryset

        if project:
            queryset = queryset.filter(team__project__name__icontains=project)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return MeetingListSerializer

        if self.action == "retrieve":
            return MeetingRetrieveSerializer

        if self.action == "create":
            return MeetingCreateSerializer

        return MeetingListSerializer

    def perform_create(self, serializer):
        serializer.save(requires_meeting_room="False")


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        day = self.request.query_params.get("day")
        room = self.request.query_params.get("room")
        project = self.request.query_params.get("project")

        queryset = self.queryset

        if day:
            day = datetime.strptime(day, "%Y-%m-%d").date()
            queryset = queryset.filter(day=day)

        if room:
            queryset = queryset.filter(room__name__icontains=room)

        if project:
            queryset = queryset.filter(
                meeting__team__project__name__icontains=project
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BookingListSerializer

        if self.action == "retrieve":
            return BookingRetrieveSerializer

        if self.action == "create":
            return BookingCreateSerializer

        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
