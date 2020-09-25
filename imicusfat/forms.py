# -*- coding: utf-8 -*-

"""
the forms we use
"""

from django import forms
from django.utils.translation import ugettext_lazy as _


class FatLinkForm(forms.Form):
    """
    fatlink form
    used to create ESI fatlinks
    """

    name_esi = forms.CharField(label=_("Fleet Name"), max_length=50)
    type_esi = forms.IntegerField(label=_("Type"), required=False)


class ManualFatForm(forms.Form):
    """
    manual fat form
    """

    character = forms.CharField(label=_("Character Name"), max_length=50)
    system = forms.CharField(label=_("System"), max_length=50)
    shiptype = forms.CharField(label=_("Ship Type"), max_length=100)


class ClickFatForm(forms.Form):
    """
    fatlink form
    used to create copy fatlinks
    """

    name = forms.CharField(label=_("Fleet Name"), max_length=50)
    duration = forms.IntegerField(label=_("Duration"), min_value=1)
    type = forms.IntegerField(label=_("Type"), required=False)


class FatLinkEditForm(forms.Form):
    """
    fatlink edit form
    used in edit view to change teh fatlink name
    """

    fleet = forms.CharField(label=_("Fleet Name"), max_length=50)
