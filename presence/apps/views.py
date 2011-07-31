import json
import logging
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
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


@login_required
def activity_ajax(request):
    activity = Activity.objects.select_related(
        'user', 'to_user'
    ).for_user(request.user)
    time = request.GET.get('time', None)
    if time:
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        activity = activity.filter(time__gt=time)

    html = render_to_string('activity_ajax.html', {'activity': activity})
    return HttpResponse(json.dumps({'html': html, 'count': activity.count()}))
