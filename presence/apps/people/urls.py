from django.conf.urls.defaults import *

urlpatterns = patterns(
    'people.views',
    url(r'^invite/$', 'invite_user',
        name="invite-user"),
)
