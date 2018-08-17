from django.db import models
from django.contrib.auth.models import User
from allianceauth.eveonline.models import EveCharacter
from django.utils import timezone

# Create your models here.


def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]


# FatLink Model
class FatLink(models.Model):
    fattime = models.DateTimeField(default=timezone.now)
    fleet = models.CharField(max_length=254)
    hash = models.CharField(max_length=254)
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return self.hash[6:]

    class Meta:
        permissions = (('manage_bfat', 'Can manage the bFAT module'),)


# PAP/FAT Model
class Fat(models.Model):
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)
    fatlink = models.ForeignKey(FatLink, on_delete=models.CASCADE)
    system = models.CharField(max_length=30)
    shiptype = models.CharField(max_length=30)
    station = models.CharField(max_length=125)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('character', 'fatlink'),)

    def __str__(self):
        return "{} - {}".format(self.fatlink, self.character)


# Log Model for Manual FAT creation
class ManualFat(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    fatlink = models.ForeignKey(FatLink, on_delete=models.CASCADE)
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)
    
    # Add property for getting the user for a character.

    def __str__(self):
        return "{} - {} ({})".format(self.fatlink, self.character, self.creator)
