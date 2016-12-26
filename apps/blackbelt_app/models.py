from __future__ import unicode_literals
from django.db import models
from ..lnr.models import User
# Create your models here.
class Friendships(models.Model):
    user = models.ForeignKey('lnr.User', models.DO_NOTHING, related_name="usersfriend")
    friendpoked = models.ForeignKey('lnr.User', models.DO_NOTHING, related_name ="friendsfriend")
