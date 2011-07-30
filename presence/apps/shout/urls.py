from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'new/$', 'shout.views.shout_new', name='shout-new'),
    url(r'^$', 'shout.views.shout_list', name='shout-list'),
    url(r'(?P<shout_id>\d+)/$', 'shout.views.shout_detail', name='shout-detail'),
)