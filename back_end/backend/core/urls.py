# pylint: disable=missing-module-docstring

from django.urls import path
from .api.svc import tile_list
from .api.svc import download


app_name = 'core'
urlpatterns = [
    # ex: /api/feedback/
    # path('feedback/', add_feedback),
    path('tile_list/', tile_list),
    path('download/', download),
]
