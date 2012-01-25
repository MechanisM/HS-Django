# -*- coding: utf-8 -*-

from django.db import models
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase
from django.utils.translation import ugettext_lazy as _

from common.utils import get_thumbnail_path


class TagsTag(TagBase):
    class Meta:
        verbose_name = _("TagsTag")
        verbose_name_plural = _("TagsTags")


class TagsTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(TagsTag, related_name="items")


class SeriesTag(TagBase):
    class Meta:
        verbose_name = _("SeriesTag")
        verbose_name_plural = _("SeriesTags")


class SeriesTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(SeriesTag, related_name="items")


class ArtistTag(TagBase):
    class Meta:
        verbose_name = _("ArtistTag")
        verbose_name_plural = _("ArtistTags")


class ArtistTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(ArtistTag, related_name="items")


class Category(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.name


class Hentai(models.Model):
    thumbnail = models.ImageField(blank=True, null=True, max_length=256,
                                  upload_to=get_thumbnail_path)
    title = models.CharField(max_length=200)
    url = models.URLField()
    download_url = models.URLField()
    category = models.ForeignKey(Category, related_name='hentais', null=True,
                                 blank=True)
    tags = TaggableManager(through=TagsTaggedItem, blank=True)
    series = TaggableManager(verbose_name=_("Series Tags"),
                             through=SeriesTaggedItem, blank=True)
    artist = TaggableManager(verbose_name=_("Artist Tags"),
                             through=ArtistTaggedItem, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
