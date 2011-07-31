from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _

from django import forms

from workflow.models import State, Project, Location


class BaseWorkflowForm(forms.Form):

    def __init__(self, user, current_state_log, *args, **kwargs):
        self._user = user
        self._current_state_log = current_state_log

        super(BaseWorkflowForm, self).__init__(*args, **kwargs)


class StateForm(BaseWorkflowForm):

    next_state = forms.ModelChoiceField(queryset=State.objects.all())

    def __init__(self, *args, **kwargs):
        super(StateForm, self).__init__(*args, **kwargs)

        self.fields['next_state'].queryset = \
            self._current_state_log.state.get_possible_next_steps()
        if 'next_state' not in self.initial:
            self.fields['next_state'].initial = \
                self._current_state_log.state.get_default_next_state()

        # if it looks like user is in current state more that maximum allowed,
        # we are asking him if he hasn't made mistake

        if self._current_state_log.state.max_duration \
        and (datetime.now() - self._current_state_log.start).total_seconds() / 60.0 > \
        self._current_state_log.state.max_duration and self.data:
            self.fields['reset_to_normal'] = forms.ChoiceField(
                choices=(
                    ('reset_to_normal', _("Sorry, I forget to change state in time")),
                    ('leave_as_it_is', _("I love to do unusual things"))
                ),
                label=_("Sorry, I forget to change state in time"),
                error_messages = {
                    'required': _("You was in previous state for unusually long time")
                }
            )

    def save(self):
        # checking if we need to set previous state log end time to 
        # it's usual duration

        if self.cleaned_data.get('reset_to_normal', 'leave_as_it_is') == 'reset_to_normal':
            time = self._current_state_log.start \
                + timedelta(minutes=self._current_state_log.state.usual_duration)
        else:
            time = None
        return self._current_state_log.change_state(
            state=self.cleaned_data['next_state'], time=time
        )


class ProjectForm(BaseWorkflowForm):

    project = forms.ModelChoiceField(queryset=Project.objects.all())

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['project'].queryset = Project.objects.filter(
            members=self._user
        )

    def save(self):
        return self._current_state_log.change_state(
            project=self.cleaned_data['project']
        )


class LocationForm(BaseWorkflowForm):

    location = forms.ModelChoiceField(queryset=Location.objects.all())

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)

        self.fields['location'].queryset = Location.objects.all()

    def save(self):
        return self._current_state_log.change_state(
            location=self.cleaned_data['location']
        )
