# meddy-news
Assignment by Meddy.com for Python developer role.


**Environment Setup (Python 3)** 
1. Create and activate virtualenv - `virtualenv venv; source venv/bin/activate`  
2. Install the requirements - `pip install -r requirements.txt`  
3. `cd` into the project directory(MeddyNews)  
4. Configure Database - `python manage.py migrate` 
5. Create superuser - `python manage.py createsuperuser` 
6. Add environment variables. See the Credentials section.
6. Start Django Dev Server - `python manage.py runserver 0:8000`  

Optional:  
_Ensure the cwd is `MeddyNews`(Django project dir) for the below steps_   
Run test cases - `python manage.py test aggregator`  
PEP8 checks - `flake8 aggregator --exclude=migrations --exclude=tests.py`

**Usage**
1. Using browser  
When hitting the api for the first time, you will be asked for username and password, use the credentials of superuser created during Environment setup.

2. Using cURL  
`curl -X GET -H 'Content-Type: application/json' -H "Authorization: Basic $(echo -n <username>:<password> | base64)" http://localhost:8000/news/`

**Credentials**  
REDDIT_USERNAME="skmycom"  
REDDIT_PASSWORD="DF@#a14saf43"  
REDDIT_CLIENTID="jwqgfZ80XhQL8A"  
REDDIT_SECRET="CFmynsMi7tNdEo98arPy2YN9eDA"  

NEWSAPI_TOKEN="86df486541ca48c9806dfb3862beb1f4"

Note:   
A temp email was used for creating reddit and newapi accounts.
