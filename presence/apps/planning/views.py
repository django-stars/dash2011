import json

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from models import DayPlan
from forms import PlanningForm

import logging

logger = logging.getLogger("presence.%s" % __name__)


@login_required
def planning(request):
    error = False
    if request.method == "POST":
        form = PlanningForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            logger.info("Planning for user %s" % request.user.username)
            messages.info(request, "New plan was added.")
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("dashboard"))
        else:
            error = True
    else:
        form = PlanningForm()

    data = {
        "form": form,
    }

    if request.method == "POST" and request.is_ajax():
        return HttpResponse(json.dumps({
            'response': 'error' if error else 'ok',
            'html': render_to_string("planning/plan-add.html", data)
        }), mimetype='application/json')
    else:
        return render_to_response("planning/plan-add.html", data,
            RequestContext(request))
