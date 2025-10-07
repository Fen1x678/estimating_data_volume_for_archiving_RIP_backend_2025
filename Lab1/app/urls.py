from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('algorithms/<int:algorithm_id>/', algorithm_page),
    path('compressions/<int:compression_id>/', compression_page),
]