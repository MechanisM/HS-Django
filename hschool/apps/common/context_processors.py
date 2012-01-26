# -*- coding: utf-8 -*-

from django.db.models import Count
from common.models import SeriesTag


def hschool(request):
    series_tags = SeriesTag.objects.annotate(items_count=Count('items')).all()
    series_tags = series_tags.order_by('-items_count')
    if series_tags:
        series_tags = series_tags[:30]

    return {'series_tags': series_tags}
