from django.conf.urls.defaults import *

urlpatterns = patterns(
    'planning.views',
    url(r'^$', 'planning', name='planning'),
)
