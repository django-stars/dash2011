from django.conf import settings
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'new/$', 'event.views.event_new', name='event-new'),
    url(r'^$', 'event.views.event_list', name='event-list'),
    url(r'(?P<event_id>\d+)/$', 'event.views.event_detail', name='event-detail'),
)
