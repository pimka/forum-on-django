from logging import getLogger

from django.conf import settings
from rest_framework.views import Request, Response

from base import BaseView
import requests


URLS = getattr(settings, 'URLS')

class UserBaseOperations(BaseView):
    logger = getLogger('gateway_user')

    def post(self, request):
        self.info(request, 'create new user')
        try:
            response = requests.post(URLS['user'], json=request.data)
            json, status = response.json(), response.status_code
        except:
            pass
