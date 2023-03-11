import os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


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
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

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
        Project,
        on_delete=models.CASCADE,
        related_name="teams"
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
        max_length=11,
        choices=NAME_CHOICES,
        default="WEEKLY"
    )

    def __str__(self):
        return self.name


class Meeting(models.Model):
    teams = models.ManyToManyField(Team, related_name="meetings")
    type_of_meeting = models.ForeignKey(
        TypeOfMeeting, on_delete=models.PROTECT, related_name="meetings"
    )
    requires_meeting_room = models.BooleanField(default=False)
