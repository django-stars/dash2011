from django import template
from django.conf import settings
from django.utils.hashcompat import md5_constructor
from django.utils.html import escape
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import urllib

from planning.models import DayPlan

register = template.Library()

GRAVATAR_URL = getattr(settings, "GRAVATAR_URL",\
    "http://www.gravatar.com/avatar/")


def gravatar(value, size=100):
    url = "%s%s?" % \
        (GRAVATAR_URL, md5_constructor(value).hexdigest())
    url += urllib.urlencode({"s": str(size)})
    return escape(url)

register.simple_tag(gravatar)


@register.inclusion_tag("people/tags/profile-info.html", takes_context=True)
def profile_info(context, username):
    user = get_object_or_404(User, username=username)
    data = {
        'user': user,
        'request': context['request']
    }
    return data
