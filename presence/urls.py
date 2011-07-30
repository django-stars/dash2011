from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html',}, name='login'),
    url(r'^logout/$', 'people.views.logout', name='logout'),
    url(r'^workflow/', include('workflow.urls')),
    url(r'^activation/', include('activation.urls')),
    url(r'^shout/', include('shout.urls')),
    url(r'^people/', include('people.urls')),
)


if settings.LOCAL_DEVELOPMENT:
    urlpatterns += staticfiles_urlpatterns()

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
