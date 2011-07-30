from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class InviteForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users:
            raise forms.ValidationError(_("User with this email already exists!"))
        return email

    def save(self):
        email = self.cleaned_data['email']
        user = User(
            username=email,
            email=email
        )
        user.save()
