# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


requires = ['Django', 'django-extensions', 'Werkzeug', 'django-taggit', 'South',
            'PIL']

setup(name='hschool',
      version='0.1',
      description='',
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      dependency_links=[
        'http://www.djangoproject.com/download/1.3.1/tarball#Django-1.3.1.tar.gz'
      ]
)
