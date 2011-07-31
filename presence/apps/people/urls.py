from django.conf.urls.defaults import *

urlpatterns = patterns(
    'people.views',
    url(r'^invite/$', 'invite_user', name='invite-user'),
    url(r'^edit/$', 'profile_edit', name='profile-edit'),
    url(r'^(?P<id>\d+)/$', 'profile_details', name='profile-details')
)
