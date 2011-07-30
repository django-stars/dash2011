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

    def save(self):
        return self._current_state_log.change_state(
            state=self.cleaned_data['next_state']
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
