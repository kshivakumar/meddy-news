"""Aggregator Views"""

from collections import OrderedDict

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings


@api_view(['GET'])
def get_news(request):
    query_params = request.query_params
    if query_params:
        return Response('News Search')
    # latest news
    return Response('Latest News')


def get_news_from_reddit(query=None):
    token = _get_reddit_token()
    headers = {"Authorization": "bearer {}".format(token),
               "User-Agent": "ShivaMeddy/1.0"}
    base_url = "https://oauth.reddit.com/r/news/"

    if query:
        response = requests.get(base_url + "search?q={}".format(query), headers=headers)
    else:
        response = requests.get(base_url + "new", headers=headers)

    results = response.json()['data']['children']  # 25 items

    news_items = []
    for item in results:
        data = item['data']

        news_item = OrderedDict()
        news_item['headline'] = data['title']
        news_item['link'] = data['url']
        news_item['source'] = 'reddit'

        news_items.append(news_item)

    return news_items


def get_news_from_newsapi(query=None):
    token = _get_newsapi_token()

    if query:
        url = "https://newsapi.org/v2/everything?language=en&sortBy=publishedAt&qInTitle={0}&apiKey&pageSize=25={1}".format(query, token)
    else:
        url = "https://newsapi.org/v2/top-headlines?language=en&sortBy=publishedAt&apiKey={}&pageSize=25".format(token)

    headers = {"User-Agent": "ShivaMeddy/1.0"}
    response = requests.get(url, headers=headers)

    results = response.json()['articles']

    news_items = []
    for item in results:
        news_item = OrderedDict()
        news_item['headline'] = item['title']
        news_item['link'] = item['url']
        news_item['source'] = 'newsapi'

        news_items.append(news_item)

    return news_items


def _get_reddit_token():
    """Get Reddit Token"""

    username = settings.REDDIT_USERNAME
    password = settings.REDDIT_PASSWORD

    client_id = settings.REDDIT_CLIENTID
    secret = settings.REDDIT_SECRET

    client_auth = requests.auth.HTTPBasicAuth(client_id, secret)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": "ShivaMeddy/1.0"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth,
                             data=post_data, headers=headers)

    token = response.json()['access_token']
    return token


def _get_newsapi_token():
    return settings.NEWSAPI_TOKEN
