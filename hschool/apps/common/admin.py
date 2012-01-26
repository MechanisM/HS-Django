# -*- coding: utf-8 -*-

from django.contrib import admin

from common.models import (Hentai, TagsTag, TagsTaggedItem, SeriesTag,
                           SeriesTaggedItem, ArtistTag, ArtistTaggedItem,
                           Category)


class HentaiAdmin(admin.ModelAdmin):
    pass

    
class TagsTaggedItemInline(admin.StackedInline):
    model = TagsTaggedItem


class TagsTagAdmin(admin.ModelAdmin):
    inlines = [TagsTaggedItemInline]


class SeriesTaggedItemInline(admin.StackedInline):
    model = SeriesTaggedItem


class SeriesTagAdmin(admin.ModelAdmin):
    inlines = [SeriesTaggedItemInline]


class ArtistTaggedItemInline(admin.StackedInline):
    model = ArtistTaggedItem


class ArtistTagAdmin(admin.ModelAdmin):
    inlines = [ArtistTaggedItemInline]


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hentai, HentaiAdmin)
admin.site.register(TagsTag, TagsTagAdmin)
admin.site.register(SeriesTag, SeriesTagAdmin)
admin.site.register(ArtistTag, ArtistTagAdmin)
admin.site.register(Category, CategoryAdmin)
