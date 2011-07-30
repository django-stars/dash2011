from django import forms

from models import UserVote


class UserVoteForm(forms.ModelForm):
    class Meta:
        model = UserVote
        exclude = ('user', 'date')
