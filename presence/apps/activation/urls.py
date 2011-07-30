from django.conf.urls.defaults import *

urlpatterns = patterns(
    'activation.views',
    url(r'^(?P<key>[-\w]+)/$', 'activate_user',
        name="activate-user"),
)
