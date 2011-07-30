import logging

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import transaction
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from workflow.models import StateLog
from workflow.forms import StateForm, ProjectForm, LocationForm


logger = logging.getLogger("presence.%s" % __name__)


@transaction.commit_on_success
def index(request, template_name="workflow/index.html"):
    """display state of current user and allow to change it"""

    current_state_log = StateLog.objects.get_user_current_state_log(
        request.user
    )
    if request.method == 'POST' and request.POST.get('is_state_form', False):
        state_form = StateForm(request.user, current_state_log, request.POST)
        if state_form.is_valid():
            new_state = state_form.save()
            messages.success(request, _("State changed to %s" % new_state.state))
            return HttpResponseRedirect(reverse('workflow-index'))
    else:
        state_form = StateForm(request.user, current_state_log)

    if request.method == 'POST' and request.POST.get('is_project_form', False):
        project_form = ProjectForm(request.user, current_state_log, request.POST)
        if project_form.is_valid():
            new_state = project_form.save()
            messages.success(request, _("Project changed to %s" % new_state.project))
            return HttpResponseRedirect(reverse('workflow-index'))
    else:
        project_form = ProjectForm(
            request.user, current_state_log,
            initial={'project': current_state_log.project}
        )

    if request.method == 'POST' and request.POST.get('is_location_form', False):
        location_form = LocationForm(request.user, current_state_log, request.POST)
        if location_form.is_valid():
            new_state = location_form.save()
            messages.success(request, _("Location changed to %s" % new_state.location))
            return HttpResponseRedirect(reverse('workflow-index'))
    else:
        location_form = LocationForm(
            request.user, current_state_log,
            initial={'location': current_state_log.location}
        )

    return render_to_response(
        template_name, 
        {
            'state_form': state_form, 'project_form': project_form,
            'location_form': location_form,
            'current_state_log': current_state_log,
        },
        context_instance=RequestContext(request)
    )
