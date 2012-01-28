# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from haystack.indexes import *
from haystack import site

from common.models import Hentai


logger = logging.getLogger("hschool")

class HentaiIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)

    def index_queryset(self):
        """ Used when the entire index for model is updated. """
        return Hentai.objects.filter(created__lte=datetime.now())

site.register(Hentai, HentaiIndex)
