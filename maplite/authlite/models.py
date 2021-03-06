"""
Models for authlite, merely for entry poi without the need to sign up, only by sending mail.
"""

from django.conf import settings
from django.db import models
import datetime
import random
import hashlib

#class SignUpProfile(models.Model):
class PoiEntryProfile(models.Model):
    email = models.EmailField()
    #signup_key = models.CharField(max_length=40)
    poientry_key = models.CharField(max_length=40)
    expiry_date = models.DateTimeField()

    class Meta:
        pass

    def __str__(self):
        return str(self.email)

    def save(self):
        # Generate activation key
        the_key = str(random.random())
        self.poientry_key = hashlib.sha1(the_key.encode('utf-8')).hexdigest()
        # Set expiry date
        self.expiry_date = datetime.datetime.now() + \
                            datetime.timedelta(settings.POIENTRY_EXPIRY_DAYS)
        super(PoiEntryProfile, self).save()
