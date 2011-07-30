from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as logout_
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.urlresolvers import reverse

from forms import InviteForm


def logout(request):
    logout_(request)
    return HttpResponseRedirect('/')


def invite_user(request):
    active_users = User.objects.filter(is_active=True)
    not_active_users = User.objects.filter(is_active=False)

    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('invite-user'))
    else:
        form = InviteForm()
    data = {
        'form': form,
        'active_users': active_users,
        'not_active_users': not_active_users
    }
    return render_to_response('people/invite.html', data,
      RequestContext(request))
