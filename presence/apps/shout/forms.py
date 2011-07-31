from django import forms
from django.forms.util import ErrorList
from shout.models import Shout
from shout.utils import is_private, user2link, url2link

class ShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        fields = ('message',)

    def save(self, *args, **kwargs):
        super(ShoutForm, self).save(*args, **kwargs)
        instance = self.instance
        instance.is_private, instance.message = is_private(instance.message)
        instance.message = user2link(instance.message)
        instance.message = url2link(instance.message)
        return instance
