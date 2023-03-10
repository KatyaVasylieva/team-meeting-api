from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MeetingRoom(models.Model):
    name = models.CharField(max_length=63)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    has_projector = models.BooleanField(default=False)
    is_soundproof = models.BooleanField(default=False)

    class Meta:
        ordering = ["capacity"]

    def __str__(self):
        return f"{self.name} ({self.capacity} {'person' if self.capacity==1 else 'people'}" \
               f"{', projector' if self.has_projector else ''}" \
               f"{', soundproof' if self.is_soundproof else ''})"
