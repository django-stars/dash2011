import logging

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import transaction
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from workflow.models import StateLog
from workflow.forms import StateForm


logger = logging.getLogger("presence.%s" % __name__)


@transaction.commit_on_success
def state(request, template_name="workflow/state.html"):
    """display state of current user and allow to change it"""

    current_state_log = StateLog.objects.get_user_current_state_log(
        request.user
    )
    if request.method == 'POST':
        form = StateForm(request.user, current_state_log, request.POST)
        if form.is_valid():
            new_state = form.change_state()
            messages.success(request, _("State changed to %s" % new_state.state))
            return HttpResponseRedirect(reverse('workflow-state'))
    else:
        form = StateForm(request.user, current_state_log)

    return render_to_response(
        template_name, {'form': form, 'current_state_log': current_state_log},
        context_instance=RequestContext(request)
    )
