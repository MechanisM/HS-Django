# -*- coding: utf-8 -*-

from django.db import models
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from common.utils import get_thumbnail_path


class TagsTag(TagBase):
    class Meta:
        verbose_name = _("Tags Tag")
        verbose_name_plural = _("Tags Tags")


class TagsTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(TagsTag, related_name="items")


class SeriesTag(TagBase):
    class Meta:
        verbose_name = _("Series Tag")
        verbose_name_plural = _("Series Tags")


class SeriesTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(SeriesTag, related_name="items")


class ArtistTag(TagBase):
    class Meta:
        verbose_name = _("Artist Tag")
        verbose_name_plural = _("Artist Tags")


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
    download_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='hentais', null=True,
                                 blank=True)
    tags = TaggableManager(through=TagsTaggedItem, blank=True)
    series = TaggableManager(verbose_name=_("Series Tags"),
                             through=SeriesTaggedItem, blank=True)
    artist = TaggableManager(verbose_name=_("Artist Tags"),
                             through=ArtistTaggedItem, blank=True)
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class Like(models.Model):
    hentai = models.ForeignKey(Hentai, related_name='likes')
    user = models.ForeignKey(User, related_name='liked_hentais',
                             blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
