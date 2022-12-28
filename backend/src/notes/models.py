from django.db import models
from app.models import RandomSlugModel, TimestampModel, IsActiveModel

class Notes(TimestampModel, RandomSlugModel, IsActiveModel):
    PREFIX = 'notes_'
    title = models.CharField(max_length=64, null=False)
    text = models.TextField(null=True)
    sentAt = models.DateTimeField(
        'Sent at', auto_now_add=True, editable=False)