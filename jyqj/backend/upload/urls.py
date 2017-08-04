# -*- coding: UTF-8 -*-

from django.conf.urls import url

from .views import upload_image, upload_file_ajax

upload_urls = [
    url(r'^image_with_type/$', upload_image, name='image'),
    url(r'^upload_file_ajax/$', upload_file_ajax, name='upload_file_ajax'),
]
