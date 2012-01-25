# -*- coding: utf-8 -*-

import os
import logging
from django.conf import settings


logger = logging.getLogger('hschool')

def get_thumbnail_path(instance, filename):
    thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'thumbnails')

    if not os.path.exists(thumbnail_dir):
        os.mkdir(thumbnail_dir)

    img_path = os.path.join(thumbnail_dir, "%s-%s" % (instance.id, filename))
    logger.debug(img_path)
    return img_path
