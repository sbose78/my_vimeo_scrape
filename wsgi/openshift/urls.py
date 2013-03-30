from django.conf.urls.defaults import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^user/(?P<username>.*)$','openshift.views.get_user_data', name='get_user_data'),
    url(r'^$', 'openshift.views.user', name='user'),
    url(r'^(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT }),

)
