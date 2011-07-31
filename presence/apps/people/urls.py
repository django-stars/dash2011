from django.conf.urls.defaults import *

urlpatterns = patterns(
    'people.views',
    url(r'^invite/$', 'invite_user', name='invite-user'),
    url(r'^edit/$', 'profile_edit', name='profile-edit'),
    url(r'^password/change/$', 'change_password', name='change-password'),
    url(r'^(?P<id>\d+)/$', 'profile_details', name='profile-details'),
    url(r'^team/$', 'team_list', name='team-list')
)
