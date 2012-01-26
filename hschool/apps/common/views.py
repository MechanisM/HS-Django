# -*- coding: utf-8 -*-

from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator
from django.db.models import Count

from common.models import Hentai, Category, SeriesTag, ArtistTag, TagsTag


def home(request):
    hentai_list = Hentai.objects.all()
    paginator = Paginator(hentai_list, 10)
    page = request.GET.get('page', 1)
    try:
        hentais = paginator.page(page)
    except PageNotAnInteger:
        hentais = paginator.page(1)
    except EmptyPage:
        hentais = paginator.page(paginator.num_pages)

    return render_to_response('common/home.html',
                              {'hentais': hentais},
                              RequestContext(request))


def series(request):
    series_tags_list = SeriesTag.objects.annotate(items_count=Count('items')).all()
    series_tags_list = series_tags_list.order_by('-items_count')

    paginator = Paginator(series_tags_list, 100)
    page = request.GET.get('page', 1)
    try:
        series_list = paginator.page(page)
    except PageNotAnInteger:
        series_list = paginator.page(1)
    except EmptyPage:
        series_list = paginator.page(paginator.num_pages)
    return render_to_response('common/series.html',
                              {'series_list': series_list},
                              RequestContext(request))


def artist(request):
    artist_tags_list = ArtistTag.objects.annotate(items_count=Count('items')).all()
    artist_tags_list = artist_tags_list.order_by('-items_count')

    paginator = Paginator(artist_tags_list, 100)
    page = request.GET.get('page', 1)
    try:
        artist_list = paginator.page(page)
    except PageNotAnInteger:
        artist_list = paginator.page(1)
    except EmptyPage:
        artist_list = paginator.page(paginator.num_pages)
    return render_to_response('common/artist.html',
                              {'artist_list': artist_list},
                              RequestContext(request))


def tags(request):
    tags_tags_list = TagsTag.objects.annotate(items_count=Count('items')).all()
    tags_tags_list = tags_tags_list.order_by('-items_count')

    paginator = Paginator(tags_tags_list, 100)
    page = request.GET.get('page', 1)
    try:
        tags_list = paginator.page(page)
    except PageNotAnInteger:
        tags_list = paginator.page(1)
    except EmptyPage:
        tags_list = paginator.page(paginator.num_pages)
    return render_to_response('common/tags.html',
                              {'tags_list': tags_list},
                              RequestContext(request))
