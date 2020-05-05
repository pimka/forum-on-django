import requests
from requests.exceptions import RequestException

from .celery import celery_app

# celery -A celery_queue worker -l info -P gevent

@celery_app.task(autoretry_for=(RequestException,), retry_kwargs={ 'max_retries' : 5 }, retry_backoff=True)
def post(url, data, header=None):
    response = requests.post(url, json=data, headers=header)
    return response

@celery_app.task(autoretry_for=(RequestException,), retry_kwargs={ 'max_retries' : 5 }, retry_backoff=True)
def patch(url, data, header=None):
    response = requests.patch(url, json=data, headers=header)
    return response

@celery_app.task(autoretry_for=(RequestException,), retry_kwargs={ 'max_retries' : 5 }, retry_backoff=True)
def delete(url, data, header=None):
    response = requests.delete(url, headers=header)
    return response

@celery_app.task(autoretry_for=(RequestException,), retry_kwargs={ 'max_retries' : 5 }, retry_backoff=True)
def put(url, data, header=None):
    response = requests.put(url, json=data, headers=header)
    return response
