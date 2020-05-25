"""Aggregator Views"""

import itertools
from collections import OrderedDict

import requests
from django.http.response import JsonResponse, HttpResponseServerError

from django.conf import settings


USER_AGENT = "Python:meddy-news:v0.1 (by Shiva Kumar)"


def get_news(request):
    query = request.GET.get('query')
    try:
        data = get_aggregated_news(query)
        return JsonResponse({'news': data})
    except NotImplementedError as e:
        data = 'Error: ' + str(e)
    except:  # noqa: E722
        data = 'Something went wrong, please try again.'

    return HttpResponseServerError(data)


def get_aggregated_news(query=None, item_count=5):
    if item_count > 50:
        raise NotImplementedError(
            'Maximum no. of news items that can be fetched in a '
            'single request: <= 50, '
            'Count requested: {}'.format(item_count))

    reddit_generator = get_news_from_reddit(query)
    newsapi_generator = get_news_from_newsapi(query)

    generators = itertools.cycle([reddit_generator, newsapi_generator])

    news = []
    links = []  # Discard news items listed by both reddit and newsapi
    while len(news) < item_count:
        news_item = next(next(generators))
        if news_item['link'] not in links:
            news.append(news_item)
            links.append(news_item['link'])

    return news


def get_news_from_reddit(query=None):
    token = _get_reddit_token()
    headers = {"Authorization": "bearer {}".format(token),
               "User-Agent": USER_AGENT}

    base_url = "https://oauth.reddit.com/r/news/"
    url = base_url + ("search?q={}".format(query) if query else "new")

    response = requests.get(url, headers=headers)

    results = response.json()['data']['children']  # Each call returns 25 items

    for item in results:
        data = item['data']

        news_item = OrderedDict()
        news_item['headline'] = data['title']
        news_item['link'] = data['url']
        news_item['source'] = 'reddit'

        yield news_item


def get_news_from_newsapi(query=None):
    token = _get_newsapi_token()

    query_params = {
        'language': 'en',
        'apiKey': token,
        'sortBy': 'publishedAt',
        'pageSize': 25
    }

    base_url = "https://newsapi.org/v2/"
    if query:
        url = base_url + "everything?"
        query_params['qInTitle'] = query
    else:
        url = base_url + "top-headlines?"

    url = url + "&".join('{}={}'.format(k, v) for k, v in query_params.items())

    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers)
    results = response.json()['articles']

    for item in results:
        news_item = OrderedDict()
        news_item['headline'] = item['title']
        news_item['link'] = item['url']
        news_item['source'] = 'newsapi'

        yield news_item


def _get_reddit_token():

    username = settings.REDDIT_USERNAME
    password = settings.REDDIT_PASSWORD

    client_id = settings.REDDIT_CLIENTID
    secret = settings.REDDIT_SECRET

    client_auth = requests.auth.HTTPBasicAuth(client_id, secret)
    post_data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.post("https://www.reddit.com/api/v1/access_token",
                             auth=client_auth, data=post_data, headers=headers)

    token = response.json()['access_token']
    return token


def _get_newsapi_token():
    return settings.NEWSAPI_TOKEN
