"""MeddyNews URL Configuration
"""
from django.urls import path, include

urlpatterns = [
    path('news/', include('aggregator.urls'))
]
