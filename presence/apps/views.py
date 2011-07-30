from django.shortcuts import render_to_response
from django.template import RequestContext

from vote.forms import UserVoteForm

def dashboard(request):
    data = {
        'form': UserVoteForm()
    }
    return render_to_response('index.html', data,
        RequestContext(request))