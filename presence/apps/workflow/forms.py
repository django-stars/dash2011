from django import forms

from workflow.models import State


class StateForm(forms.Form):

    next_state = forms.ModelChoiceField(queryset=State.objects.all())

    def __init__(self, user, current_state_log, *args, **kwargs):
        self._user = user
        self._current_state_log = current_state_log

        super(StateForm, self).__init__(*args, **kwargs)

        self.fields['next_state'].queryset = \
            current_state_log.state.get_possible_next_steps()
        if 'next_state' not in self.initial:
            self.fields['next_state'].initial = \
                current_state_log.state.get_default_next_state()

    def change_state(self):
        return self._current_state_log.change_state(
            self.cleaned_data['next_state']
        )
