from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as logout_
from django.contrib.auth.models import User
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


from forms import InviteForm, ProfileEditForm, PasswordChangeForm
from activity.models import Activity

import logging

logger = logging.getLogger("presence.%s" % __name__)


def logout(request):
    logout_(request)
    return HttpResponseRedirect('/')


@login_required
def invite_user(request):
    active_users = User.objects.filter(is_active=True)
    not_active_users = User.objects.filter(is_active=False)

    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("Invited new user with email %s" % \
                form.cleaned_data['email']
                )
            messages.info(request, _("Invite email was send for %s" % \
                form.cleaned_data['email'])
                )
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


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.user.username, request.POST,
            instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "Your profile was saved")
            logger.info("User %s saved his profile" % request.user)
            return HttpResponseRedirect(reverse('profile-edit'))
    else:
        form = ProfileEditForm(request.user.username, instance=request.user)

    return render_to_response('people/profile-edit.html', {'form': form},
        RequestContext(request))


@login_required
def change_password(request):
    user = request.user
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            logger.info("Changed password for user %s" % user.username)
            messages.info(request, "Password was changed!")
    else:
        form = PasswordChangeForm()
    
    data = {
        'form': form
    }
    return render_to_response('people/change-password.html', data,
        RequestContext(request))

@login_required
def profile_details(request, id):
    user = get_object_or_404(User, id=id)

    data = {
        "user": user,
        "activity": Activity.objects.by_user(user)
    }
    return render_to_response('people/profile-details.html', data,
        RequestContext(request))


@login_required
def team_list(request):
    users = User.objects.filter(is_active=True)

    data = {
        'users': users,
    }

    return render_to_response('people/team.html', data,
        RequestContext(request))
