"""Unit Tests"""

from unittest import mock

from django.test import SimpleTestCase, Client

from aggregator import views


client = Client()


class MockedResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


class AggregatedNewsAPITest(SimpleTestCase):

    @mock.patch('aggregator.views.get_aggregated_news')
    def test_get_aggregated_news(self, mock_agg_news):
        mock_agg_news.return_value = {'ok': 'good'}
        response = client.get('/news/')

        assert response.json() == {'news': {'ok': 'good'}}
        assert response.status_code == 200

    @mock.patch('aggregator.views.get_aggregated_news')
    def test_get_aggregated_news_notimplemented(self, mock_agg_news):
        mock_agg_news.side_effect = NotImplementedError('nie')
        response = client.get('/news/')

        assert response.content == b'Error: nie'
        assert response.status_code == 500

    @mock.patch('aggregator.views.get_aggregated_news')
    def test_get_aggregated_news_unhandled_exception(self, mock_agg_news):
        mock_agg_news.side_effect = Exception('Boom Boom!!')
        response = client.get('/news/')

        assert response.content == b'Something went wrong, please try again.'
        assert response.status_code == 500


class AggregatedNewsTest(SimpleTestCase):

    @mock.patch('aggregator.views.get_news_from_reddit')
    @mock.patch('aggregator.views.get_news_from_newsapi')
    def test_get_aggregated_news(self, mock_newsapi, mock_reddit):
        mock_newsapi.return_value = ({'link': l} for l in ['n1', 'n2'])
        mock_reddit.return_value = ({'link': l} for l in ['r1', 'r2'])
        actual = views.get_aggregated_news(item_count=4)

        assert actual == [{'link': 'r1'}, {'link': 'n1'}, {'link': 'r2'}, {'link': 'n2'}]

    @mock.patch('aggregator.views.get_news_from_reddit')
    @mock.patch('aggregator.views.get_news_from_newsapi')
    def test_get_aggregated_news_duplicate_links(self, mock_newsapi, mock_reddit):
        mock_newsapi.return_value = ({'link': l} for l in ['l', 'n2'])
        mock_reddit.return_value = ({'link': l} for l in ['r1', 'l'])

        actual = views.get_aggregated_news(item_count=3)

        assert actual == [{'link': 'r1'}, {'link': 'l'}, {'link': 'n2'}]

    def test_get_aggregated_news_notimplementederror(self):
        self.assertRaises(NotImplementedError, views.get_aggregated_news, item_count=51)


class RedditAPITest(SimpleTestCase):

    @mock.patch('requests.auth.HTTPBasicAuth')
    @mock.patch('requests.post')
    def test_ing(self, mock_post, mock_auth):
        mocked = MockedResponse(200, {"access_token": 199})

        mock_auth.return_value = mocked
        mock_post.return_value = mocked

        res = views._get_reddit_token()

        assert res == 199

    @mock.patch('aggregator.views._get_reddit_token')
    @mock.patch('requests.get')
    def test_get_news_from_reddit_top(self, mock_requests, mock_token):
        mock_token.return_value = 'token'

        json_data = {
            'data': {'children': [
                {
                    'data': {
                        'title': 'R1',
                        'url': 'R URL1'
                    }
                }
            ]}
        }
        mock_requests.return_value = MockedResponse(status_code=200, json_data=json_data)

        actual = views.get_news_from_reddit()

        assert next(actual) == {
            'headline': 'R1',
            'link': 'R URL1',
            'source': 'reddit'
        }

    @mock.patch('aggregator.views._get_reddit_token')
    @mock.patch('requests.get')
    def test_get_news_from_reddit_search(self, mock_requests, mock_token):
        mock_token.return_value = 'token'

        json_data = {
            'data': {'children': [
                {
                    'data': {
                        'title': 'R2',
                        'url': 'R URL2'
                    }
                }
            ]}
        }
        mock_requests.return_value = MockedResponse(status_code=200, json_data=json_data)

        actual = views.get_news_from_reddit('bitcoin')

        assert next(actual) == {
            'headline': 'R2',
            'link': 'R URL2',
            'source': 'reddit'
        }

        assert mock_requests.call_args_list[0][0] == \
               ("https://oauth.reddit.com/r/news/search?q=bitcoin",)


class NewsAPITest(SimpleTestCase):

    @mock.patch('aggregator.views._get_newsapi_token')
    @mock.patch('requests.get')
    def test_get_news_from_newsapi_top(self, mock_requests, mock_token):
        mock_token.return_value = 'token'

        json_data = {
            'articles': [
                {
                    'title': 'N1',
                    'url': 'N URL1'
                }
            ]}

        mock_requests.return_value = MockedResponse(status_code=200, json_data=json_data)

        actual = views.get_news_from_newsapi()

        assert next(actual) == {
            'headline': 'N1',
            'link': 'N URL1',
            'source': 'newsapi'
        }

        assert mock_requests.call_args_list[0][0] == \
               ("https://newsapi.org/v2/top-headlines?language=en&apiKey=token&sortBy=publishedAt&pageSize=25",)

    @mock.patch('aggregator.views._get_newsapi_token')
    @mock.patch('requests.get')
    def test_get_news_from_newsapi_search(self, mock_requests, mock_token):
        mock_token.return_value = 'token'

        json_data = {
            'articles': [
                {
                    'title': 'N2',
                    'url': 'N URL2'
                }
            ]}

        mock_requests.return_value = MockedResponse(status_code=200, json_data=json_data)

        actual = views.get_news_from_newsapi('netflix')

        assert next(actual) == {
            'headline': 'N2',
            'link': 'N URL2',
            'source': 'newsapi'
        }

        assert mock_requests.call_args_list[0][0] == \
               ("https://newsapi.org/v2/everything?language=en&apiKey=token&sortBy=publishedAt&pageSize=25&qInTitle=netflix",)
