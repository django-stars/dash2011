from datetime import datetime

from django import template

from workflow.models import StateLog
from workflow.forms import StateForm, ProjectForm, LocationForm


register = template.Library()


@register.inclusion_tag('workflow/_form.html', takes_context=True)
def workflow_forms(context):
    request = context['request']
    current_state_log = StateLog.objects.get_user_current_state_log(
        request.user
    )
    state_form = StateForm(request.user, current_state_log)
    project_form = ProjectForm(
        request.user, current_state_log,
        initial={'project': current_state_log.project}
    )
    location_form = LocationForm(
        request.user, current_state_log,
        initial={'location': current_state_log.location}
    )

    return {
        'state_form': state_form,
        'project_form': project_form,
        'location_form': location_form,
        'current_state_log': current_state_log,
    }
