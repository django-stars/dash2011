from django import forms
from django.forms.util import ErrorList
from shout.models import Shout
from shout.utils import is_private

class ShoutForm(forms.ModelForm):
	class Meta:
		model = Shout
		fields = ('message',)
		#widgets = {
		#	'message': forms.TextInput
		#}

	def save(self, *args, **kwargs):
		super(ShoutForm, self).save(*args, **kwargs)
		instance = self.instance
		instance.is_private, instance.message = is_private(instance.message)
		return instance