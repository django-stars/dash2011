from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'$', view=views.state, name='workflow-state'),
)
