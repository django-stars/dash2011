import re
from lxml import html

from django.contrib.auth.models import User
from django.conf import settings


CONVERT_URLS = getattr(settings, 'SHOUT_CONVERT_URL', True)

USER_RE = re.compile(r'@(?P<user>[\d\w_]+)', re.M|re.U|re.I|re.S)
LINK_RE= re.compile(r'(?P<link>https?://[^\s]+)', re.M|re.I|re.U|re.S)


def url2link(message):
    """
    >>> message1 = "Go to http://google.com. Or http://google.com.ua/, http://google.ua!"
    >>> url2link(message1)
    'Go to <a href="http://google.com">http://google.com</a>. Or <a href="http://google.com">http://google.com</a>.ua/, <a href="http://google.ua">http://google.ua</a>!'
    """
    links = LINK_RE.findall(message)
    for link in links:
        link = link[:-1] if link[-1] in ('.', ',', '!', '?') else link
        title = link
        if CONVERT_URLS:
            try:
                title = html.parse(link).find(".//title").text
                title = title if title else link
            except (AttributeError, AssertionError, IOError):
                pass
        message = message.replace(link, '<a href="%s">%s</a>' % (link, title))
    return message


def is_private(message):
    """
    >>> message1 = "!! this is secret message"
    >>> message2 = "! this is not secret message"
    >>> message3 = " !! this is also not secret message"
    >>> is_private(message1)
    (True, 'this is secret message')
    >>> is_private(message2)
    (False, '! this is not secret message')
    >>> is_private(message3)
    (False, ' !! this is also not secret message')
    """
    result = message.startswith("!! ")
    return result, message[3:] if result else message


def user2link(message):
    users = USER_RE.findall(message)
    for user in users:
        try:
            django_user = User.objects.get(username=user)
            user_link = '<a href="%s">@%s</a>' % (django_user.get_absolute_url(), django_user.get_full_name() or django_user.username)
            message = message.replace('@%s' % user, user_link)
        except User.DoesNotExist:
            pass
    return message
