from django import forms
from django.utils.translation import ugettext_lazy as _

from models import DayPlan


class PlanningForm(forms.ModelForm):
    class Meta:
        model = DayPlan
        fields = ('date', 'work_status', 'start_date', 'end_date')

    def clean_work_status(self):
        work_status = self.cleaned_data['work_status']
        try:
            start_date = self.cleaned_data['start_date']
        except KeyError:
            start_date = None

        try:
            end_date = self.cleaned_data['end_date']
        except KeyError:
            end_date = None

        if work_status == 'a' and not \
            all([start_date, end_date]):
            raise forms.ValidationError(
                _("Start and End date need be defined!")
                )
        else:
            return work_status
