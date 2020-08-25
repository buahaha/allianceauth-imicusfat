# -*- coding: utf-8 -*-
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger

from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

from . import __title__
from .utils import LoggerAddTag


logger = LoggerAddTag(get_extension_logger(__name__), __title__)


# Create your models here.
def get_sentinel_user():
    return User.objects.get_or_create(username="deleted")[0]


# Abstract model to allow for soft deletion
class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


# Fat Link type (StratOp, ADM, HD etc)
class IFatLinkType(SoftDeletionModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.name)


# FatLink Model
class IFatLink(SoftDeletionModel):
    ifattime = models.DateTimeField(default=timezone.now)
    fleet = models.CharField(max_length=254, null=True)
    hash = models.CharField(max_length=254)
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    deleted_at = models.DateTimeField(blank=True, null=True)
    link_type = models.ForeignKey(IFatLinkType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.hash[6:]

    class Meta:
        permissions = (
            ("manage_imicusfat", "Can manage the imicusfat module"),
            ("stats_corp_own", "Can see own corp stats"),
            ("stats_corp_other", "Can see stats of other corps."),
            (
                "stats_char_other",
                "Can see stats of characters not associated with current user.",
            ),
        )
        ordering = ("-ifattime",)


# Clickable Link Duration Model
class ClickIFatDuration(models.Model):
    duration = models.PositiveIntegerField()
    fleet = models.ForeignKey(IFatLink, on_delete=models.CASCADE)


# PAP/FAT Model
class IFat(SoftDeletionModel):
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)
    ifatlink = models.ForeignKey(IFatLink, on_delete=models.CASCADE)
    system = models.CharField(max_length=100, null=True)
    shiptype = models.CharField(max_length=100, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = (("character", "ifatlink"),)

    def __str__(self):
        return "{} - {}".format(self.ifatlink, self.character)


# Log Model for Manual FAT creation
class ManualIFat(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    ifatlink = models.ForeignKey(IFatLink, on_delete=models.CASCADE)
    character = models.ForeignKey(EveCharacter, on_delete=models.CASCADE)

    # Add property for getting the user for a character.

    def __str__(self):
        return "{} - {} ({})".format(self.ifatlink, self.character, self.creator)


# Log Model for Deletion of Fats and FatLinks
class DelLog(models.Model):
    # 0 for FatLink, 1 for Fat
    deltype = models.BooleanField(default=0)
    remover = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    string = models.CharField(max_length=100)

    def delt_to_str(self):
        if self.deltype == 0:
            return "IFatLink"
        else:
            return "IFat"

    def __str__(self):
        return "{}/{} - {}".format(self.delt_to_str(), self.string, self.remover)
