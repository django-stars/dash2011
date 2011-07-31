from django import forms
from django.forms.util import ErrorList
from event.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
