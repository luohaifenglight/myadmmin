# =========== coding:utf8 =========
from django.conf.urls import url,include
from .views import level_manager,LevelManagerDTView,level_edit,sublevel_edit,sublevel_add


musicballoon_urls = [
    url(r'^level_manager/$', level_manager, name='level_manager'),
    url(r'^level_manager/edit/$', level_edit, name='level_edit'),
    url(r'^level_manager/sublevel_edit/$', sublevel_edit, name='sublevel_edit'),
    url(r'^level_manager/sublevel_add/$', sublevel_add, name='sublevel_add'),
    # url(r'^level_manager/sublevel_create/$', level_create, name='level_create'),
    url(r'^datatable/$', LevelManagerDTView.as_view(), name='level_manager_table')
]

