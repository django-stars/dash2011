from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from vote.forms import UserVoteForm
from vote.models import UserVote

import logging

logger = logging.getLogger("presence.%s" % __name__)

@login_required
def dashboard(request):
    data = {
        'form': UserVoteForm()
    }
    return render_to_response('index.html', data,
        RequestContext(request))