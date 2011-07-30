from django import template
from django.conf import settings
from django.utils.hashcompat import md5_constructor
from django.utils.html import escape

import urllib

register = template.Library()

GRAVATAR_URL = getattr(settings, "GRAVATAR_URL",\
    "http://www.gravatar.com/avatar/")


def gravatar(value, size=100):
    url = "%s%s?" % \
        (GRAVATAR_URL, md5_constructor(value).hexdigest())
    url += urllib.urlencode({"s": str(size)})
    return escape(url)

register.simple_tag(gravatar)
