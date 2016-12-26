from __future__ import unicode_literals
from django.db import models
import bcrypt
import re, time, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
DATE = re.compile('((0[1-9])|(1[0-2]))[\/]((0[1-9])|(1[0-9])|(2[0-9])|(3[0-1]))[\/](\d{4})')

# Create your models here.
class UserManager(models.Manager):
    def validateemail(self, email):
        if not EMAIL_REGEX.match(email):
            return "fail"
        else:
            return "pass"
    def date(self,date):
        if not DATE.match(date):
            return "fail"
        else:
            return "pass"
    def datecheck(self, date):
        if time.strptime(datetime.datetime.now().strftime("%m/%d/%Y"),"%m/%d/%Y") <time.strptime(date,"%m/%d/%Y"):
            return "fail"
        else:
            return "pass"
    def get(self,email):
        try:
            User.objects.get(email = email)
            return email
        except:
            return "fail"
    def cryptfy(self,password):
        hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        return hashed

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    userManager = UserManager()
    objects = models.Manager()
    birthdate = models.CharField(max_length=100)
