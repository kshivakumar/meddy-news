"""Aggregator Views"""

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_news(request):
    query_params = request.query_params
    if query_params:
        return Response('News Search')
    # latest news
    return Response('Latest News')
