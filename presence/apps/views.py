import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from vote.forms import UserVoteForm
from vote.models import UserVote
from activity.models import Activity

logger = logging.getLogger("presence.%s" % __name__)

@login_required
def dashboard(request):
    activity = Activity.objects.select_related(
        'user', 'to_user'
    ).for_user(request.user)
    data = {
        'form': UserVoteForm(),
        'activity': activity
    }
    return render_to_response('index.html', data,
        RequestContext(request)
    )
