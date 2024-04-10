from email.policy import default
import uuid

from django.contrib.gis.db import models
from django.db.models.functions import Now
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.contrib.auth.models import User
# from django.db import models
# Create your models here.

def is_valid_point(point: Point):
    if not (-90 <= point.x <= 90 and -180 <= point.y < 180):
        raise ValidationError("Not valid coordinates")
    
def filename(ins: models.Model, filename: str):
    return "photos/{0}.{1}".format(uuid.uuid4(), filename.split(".")[-1])


class Treasure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.PointField(geography=True, validators=[is_valid_point], srid=4326)
    description = models.TextField(max_length=1000, validators=[MinLengthValidator(10)])
    date_posted = models.DateTimeField(default=timezone.now, db_default=Now(), editable=False)
    class Status(models.IntegerChoices):
        POSTED = 0
        RECEIVED = 1
        FOUND = 2
    status = models.IntegerField(choices=Status, editable=False, default=Status.POSTED)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(db_default=True)
    new = models.BooleanField(db_default=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    protected = models.BooleanField(db_default=False)

class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    treasure = models.ForeignKey(Treasure, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=filename)

