# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from haystack.views import SearchView

from common.models import (Hentai, Category, SeriesTag, ArtistTag, TagsTag,
                           Like)


def home(request):
    hentai_list = Hentai.objects.all().order_by('-created')
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


def tag_detail(request, tag_type=None, tag_id=None):
    if not tag_type or not tag_id:
        return HttpResponseRedirect(reverse("home"))
    tags_dict = {'series': SeriesTag,
                 'artist': ArtistTag,
                 'tags': TagsTag}
    tag = get_object_or_404(tags_dict[tag_type], id=tag_id)
    hentai_list = tag.items.all().order_by('hentai__title')

    paginator = Paginator(hentai_list, 10)
    page = request.GET.get('page', 1)
    try:
        hentais = paginator.page(page)
    except PageNotAnInteger:
        hentais = paginator.page(1)
    except EmptyPage:
        hentais = paginator.page(paginator.num_pages)
    return render_to_response('common/tagged_items.html',
                              {'hentais': hentais, 'current_tag': tag.name},
                              RequestContext(request))


def search(request):
    search_view = HSchoolSearchView()
    search_view.fetch_results(request)
    return search_view.create_response()


class HSchoolSearchView(SearchView):
    def __call__(self, request):
        """ Override __call__ so it doesn't return response immediately. """
        pass

    def fetch_results(self, request):
        self.request = request
        
        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

    def extra_context(self):
        return {'results_count': len(self.results)}


def like(request, hentai_id):
    hentai = get_object_or_404(Hentai, id=hentai_id)
    like = Like(hentai=hentai)
    like.save()
    return HttpResponseRedirect(request.GET.get('destination', '/'))


def featured(request):
    hentai_list = Hentai.objects.filter(is_featured=True).order_by('-created')
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


def most_liked(request):
    start_date = datetime.now() - timedelta(days=30)
    hentai_list = Hentai.objects.filter(likes__created__gte=start_date)
    hentai_list = hentai_list.annotate(likes_count=Count('likes'))
    hentai_list = hentai_list.order_by('-likes_count')
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
