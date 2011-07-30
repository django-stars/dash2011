from django.conf.urls.defaults import *

urlpatterns = patterns(
    'vote.views',
    url(r'^vote/$', 'vote',
        name="vote"),
)
