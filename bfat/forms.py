from django import forms
from django.utils.translation import ugettext_lazy as _


class FatLinkForm(forms.Form):
    fleet = forms.CharField(label=_('Fleet Name'), max_length=50)


class FlatListForm(forms.Form):
    flatlist = forms.CharField(widget=forms.Textarea)
