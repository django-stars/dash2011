from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class InviteForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users:
            raise forms.ValidationError(
                _("User with this email already exists!")
                )
        return email

    def save(self):
        email = self.cleaned_data['email']
        user = User(
            username=email,
            email=email
        )
        user.save()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, username, *args, **kwargs):
        self._username = username
        super(ProfileEditForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.get(username=username)
        if users and (username != self._username):
            raise forms.ValidationError(_("This username is already taken!"))
        return username


class PasswordChangeForm(forms.Form):
    password = forms.CharField(_("Password"),
        widget=forms.PasswordInput)
    password1 = forms.CharField(_("Repeat password"),
        widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password1 != password1:
            raise forms.ValidationError(_("Passwords doesn't match!"))
        return self.cleaned_data
