import logging

from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from event.models import Event
from event.forms import EventForm

logger = logging.getLogger("presence.%s" % __name__)

@login_required
def event_new(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return HttpResponseRedirect(reverse('event-list'))
    else:
        form = EventForm()
    
    data = {
        'form': form,
    }
    return render_to_response('event/new.html', data, RequestContext(request))

@login_required
def event_list(request):
    events = Event.published.all()
    
    data = {
        'events': events
    }
    return render_to_response('event/list.html', data, RequestContext(request))

@login_required
def event_detail(request, event_id):
    try:
        event = Event.published.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404
    
    data = {
        'event': event,
    }
    return render_to_response('event/detail.html', data, RequestContext(request))