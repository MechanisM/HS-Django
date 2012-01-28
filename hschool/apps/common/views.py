# -*- coding: utf-8 -*-

import logging
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


logger = logging.getLogger("hschool")

def home(request):
    new_list = Hentai.objects.all().order_by('-created')

    featured_list = new_list.filter(is_featured=True).order_by('-created')

    start_date = datetime.now() - timedelta(days=30)
    mostliked_list = new_list.filter(likes__created__gte=start_date)
    mostliked_list = mostliked_list.annotate(likes_count=Count('likes'))
    mostliked_list = mostliked_list.order_by('-likes_count')

    new_paginator = Paginator(new_list, 10)
    featured_paginator = Paginator(featured_list, 10)
    mostliked_paginator = Paginator(mostliked_list, 10)

    tab = request.GET.get('tab', 'new')
    page = request.GET.get('page', 1)

    # new
    try:
        if tab == 'new':
            new = new_paginator.page(page)
        else:
            raise PageNotAnInteger
    except PageNotAnInteger:
        new = new_paginator.page(1)
    except EmptyPage:
        new = new_paginator.page(new_paginator.num_pages)

    # featured
    try:
        if tab == 'featured':
            featured = featured_paginator.page(page)
        else:
            raise PageNotAnInteger
    except PageNotAnInteger:
        featured = featured_paginator.page(1)
    except EmptyPage:
        featured = featured_paginator.page(featured_paginator.num_pages)

    # most liked
    try:
        if tab == 'mostliked':
            mostliked = mostliked_paginator.page(page)
        else:
            raise PageNotAnInteger
    except PageNotAnInteger:
        mostliked = mostliked_paginator.page(1)
    except EmptyPage:
        mostliked = mostliked_paginator.page(mostliked_paginator.num_pages)

    return render_to_response('common/home.html',
                              {'new': new, 'featured': featured,
                               'mostliked': mostliked, 'tab': tab},
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

    has_liked = bool(request.COOKIES.get('has_liked', False))
    if has_liked and request.user.is_anonymous():
        return HttpResponseRedirect(request.GET.get('destination', '/'))
    else:
        like_q = hentai.likes.filter(user=request.user)
        if like_q.count() > 0:
            return HttpResponseRedirect(request.GET.get('destination', '/'))

    if request.user.is_anonymous():
        like = Like(hentai=hentai)
    else:
        like = Like(hentai=hentai, user=request.user)
    like.save()
    response = HttpResponseRedirect(request.GET.get('destination', '/'))
    response.set_cookie("has_liked", True)
    return response
