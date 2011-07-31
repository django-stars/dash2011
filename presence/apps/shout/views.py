import logging
import json

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

from shout.models import Shout
from shout.forms import ShoutForm

logger = logging.getLogger("presence.%s" % __name__)

@login_required
def shout_new(request):
    if request.method == "POST":
        form = ShoutForm(request.POST)
        if form.is_valid():
            shout = form.save(user=request.user)
            logger.info('New %s shout from "%s"' % (('public', 'private')[shout.is_private], shout.user.username))
            if request.is_ajax():
                return HttpResponse(json.dumps({'response': 'OK'}), mimetype='application/json')
            return HttpResponseRedirect(reverse('shout-list'))
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps({'response': 'ERR', 'reason': 'Shout text is required!'}), mimetype='application/json')
    else:
        form = ShoutForm()
    
    data = {
        'form': form,
    }
    return render_to_response('shout/new.html', data, RequestContext(request))


@login_required
def shout_list(request):
    #custom manager to get non provat or privat but my
    shouts = Shout.objects.filter_for_user(user=request.user)

    data = {
        'shouts': shouts,
    }
    return render_to_response('shout/list.html', data, RequestContext(request))


@login_required
def shout_detail(request, shout_id):
    try:
        shout = Shout.objects.get_for_user(user=request.user, id=shout_id)
    except Shout.DoesNotExist:
        raise Http404
    
    data = {
        'shout': shout,
    }
    return render_to_response('shout/detail.html', data, RequestContext(request))