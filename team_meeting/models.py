import os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from team_meeting_service import settings


class MeetingRoom(models.Model):
    name = models.CharField(max_length=63)
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    has_projector = models.BooleanField(default=False)
    is_soundproof = models.BooleanField(default=False)

    class Meta:
        ordering = ["capacity"]

    def __str__(self):
        return (
            f"{self.name} ({self.capacity} "
            f"{'person' if self.capacity==1 else 'people'}"
            f"{', projector' if self.has_projector else ''}"
            f"{', soundproof' if self.is_soundproof else ''})"
        )


def project_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/projects/", filename)


class Project(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to=project_image_file_path)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=63)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="teams"
    )
    num_of_members = models.IntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TypeOfMeeting(models.Model):
    NAME_CHOICES = (
        ("DAILY", "Daily meeting"),
        ("WEEKLY", "Weekly meeting"),
        ("URGENT", "Urgent meeting"),
        ("CLIENT", "Meeting with client"),
        ("CELEBRATION", "Celebration"),
    )

    name = models.CharField(
        max_length=11, choices=NAME_CHOICES, default="WEEKLY"
    )

    def __str__(self):
        return self.name


class Meeting(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="meetings"
    )
    type_of_meeting = models.ForeignKey(
        TypeOfMeeting, on_delete=models.PROTECT, related_name="meetings"
    )
    requires_meeting_room = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type_of_meeting} of {self.team}"


class Booking(models.Model):
    room = models.ForeignKey(
        MeetingRoom, on_delete=models.CASCADE, related_name="bookings"
    )
    day = models.DateField()
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    meeting = models.OneToOneField(
        Meeting, on_delete=models.CASCADE, related_name="booking"
    )

    class Meta:
        ordering = ["room", "-start_hour"]

    @staticmethod
    def validate_time(id, day, start_hour, end_hour, room, error_to_raise):
        bookings_start_in_range = Booking.objects.filter(
            day=day, room=room, start_hour__range=(start_hour, end_hour - 1)
        ).exclude(id=id)
        bookings_end_in_range = Booking.objects.filter(
            day=day, room=room, end_hour__range=(start_hour + 1, end_hour)
        ).exclude(id=id)
        if bookings_start_in_range:
            raise error_to_raise(
                "Your meeting end time conflicts with another meeting"
            )
        if bookings_end_in_range:
            raise error_to_raise(
                "Your meeting start time conflicts with another meeting"
            )

    def clean(self):
        Booking.validate_time(
            self.id,
            self.day,
            self.start_hour,
            self.end_hour,
            self.room,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Booking, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{self.meeting} ({self.room.name} meeting room, "
            f"{self.day} {self.start_hour}:00-{self.end_hour}:00)"
        )
