# A Simple Django application that lists top news items from NewsAPI and Reddit(/r/news)

## Setup
### Docker
1. Build the image  
`docker build -t meddy-news https://github.com/kshivakumar/meddy-news.git#master:.`
2. Launch the container(and the application)   
`docker run -p 8005:8005 meddy-news`

### Local 
1. Create(in a separate directory) and activate virtualenv  
  a. `virtualenv mnvenv` or `python3 -m venv mnvenv`  
  b. `source mnvenv/bin/activate`  
2. Install the requirements - `pip install -r requirements.txt`  
3. Start Django Dev Server - `python manage.py runserver 0:8005`  

Optional:    
- Run test cases - `python manage.py test`  
- PEP8 checks - `flake8 aggregator --exclude=migrations --exclude=tests.py`

## Usage
1. Using browser  
Go to `localhost:8000/news/`

2. Using cURL  
`curl -X GET localhost:8000/news/`

### What's with the name?
This was originally an assignment by meddy.com for Python Developer role.   
Original requirements:
> For this assignment you have to implement an application that aggregates news from two different APIs. The APIs you'll be using are Reddit and News API. This application should be running on your localhost and serve the result in JSON format from an endpoint whenever it gets a request. The two functionalities that need to be implemented are "list" and "search".  
