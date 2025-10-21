from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('algorithms/<int:algorithm_id>/', algorithm_page, name="algorithm_page"),
    path('compressions/<int:compression_id>/', compression_page, name="compression_page"),
    path('algorithms/<int:algorithm_id>/add_to_compression/', add_algorithm_to_draft_compression,
         name="add_algorithm_to_draft_compression"),
    path('compressions/<int:compression_id>/delete/', delete_compression, name="delete_compression")
]
