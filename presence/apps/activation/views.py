from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings

from models import ActivationKey


def activate_user(request, key):
    try:
        _key = ActivationKey.objects.activate_user(key)
    except:
        messages.error(request, "Invalid key, please login with this form")
        return HttpResponseRedirect(reverse("login"))
    else:
        _user = authenticate(key=key)
        login(request, _user)
        _key.delete()
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
