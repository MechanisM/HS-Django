# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'common.views.home', name='home'),
    url(r'^series/$', 'common.views.series', name='series'),
    url(r'^artist/$', 'common.views.artist', name='artist'),
    url(r'^tags/$', 'common.views.tags', name='tags'),
    url(r'^tags/(?P<tag_type>\w+)/(?P<tag_id>\d+)$', 'common.views.tag_detail', name='tag_detail'),
    url(r'^search/$', 'common.views.search', name='hentai_search'),
    url(r'^like/(?P<hentai_id>\d+)$', 'common.views.like', name='like'),
)

# in DEBUG mode, serve media files through Django.
if settings.DEBUG:
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
