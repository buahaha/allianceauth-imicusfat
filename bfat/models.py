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
    fleet = models.CharField(max_length=254, null=True)
    hash = models.CharField(max_length=254)
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return self.hash[6:]

    class Meta:
        permissions = (('manage_bfat', 'Can manage the bFAT module'),
                       ('stats_corp_own', 'Can see own corp stats'),
                       ('stats_corp_other', 'Can see stats of other corps.'),
                       ('stats_char_other', 'Can see stats of characters not associated with current user.'))


# Clickable Link Duration Model
class ClickFatDuration(models.Model):
    duration = models.PositiveIntegerField()
    fleet = models.ForeignKey(FatLink, on_delete=models.CASCADE)


# PAP/FAT Model
class Fat(models.Model):
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)
    fatlink = models.ForeignKey(FatLink, on_delete=models.CASCADE)
    system = models.CharField(max_length=100, null=True)
    shiptype = models.CharField(max_length=100, null=True)

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


# Log Model for Deletion of Fats and FatLinks
class DelLog(models.Model):
    # 0 for FatLink, 1 for Fat
    deltype = models.BooleanField(default=0)
    remover = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    string = models.CharField(max_length=100)

    def delt_to_str(self):
        if self.deltype == 0:
            return 'FatLink'
        else:
            return 'Fat'

    def __str__(self):
        return '{}/{} - {}'.format(self.delt_to_str(), self.string, self.remover)