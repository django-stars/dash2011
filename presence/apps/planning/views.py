from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from models import DayPlan
from forms import PlanningForm

import logging

logger = logging.getLogger("presence.%s" % __name__)


@login_required
def planning(request):
    if request.method == "POST":
        form = PlanningForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            logger.info("Planning for user %s" %  request.user.username)
            messages.info(request, "New plan was added.")
            return HttpResponseRedirect(reverse("dashboard"))
    else:
        form = PlanningForm()

    data = {
        "form": form,
    }

    return render_to_response("planning/plan-add.html", data,
        RequestContext(request))
