from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings

from models import ActivationKey

import logging

logger = logging.getLogger("presence.%s" % __name__)


def activate_user(request, key):
    try:
        _key = ActivationKey.objects.activate_user(key)
        messages.info(request,
            "Your account was activated, please change your profile!"
            )
        logger.info("User was activated with key %s" % key)
    except:
        messages.error(request, "Invalid key, please login with this form")
        logger.debug("Invalid key %s" % key)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        _user = authenticate(key=key)
        login(request, _user)
        _key.delete()
        return HttpResponseRedirect(reverse("profile-edit"))
