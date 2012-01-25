# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'common.views.home', name='home'),
)

# in DEBUG mode, serve media files through Django.
if settings.DEBUG:
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
