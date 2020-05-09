import uuid

from django.urls import reverse
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

from .models import MessageModel
from .views import MessageAdvancedOperations, MessageBaseOperations


class MessagesTestCase(APITestCase):
    def setUp(self):
        self.messages = 'messages', MessageBaseOperations.as_view()
        self.message = 'message', MessageAdvancedOperations.as_view()
        self.factory = APIRequestFactory()
        self.user_uuid = uuid.uuid4()
        self.user_auth = {'uuid': str(
            self.user_uuid), 'username': 'username', 'token': 'token', 'is_staff': False}
        self.data = {'user_uuid': self.user_uuid,
                     'head_uuid': uuid.uuid4(), 'body': 'meh'}

    def test_post_message(self):
        url, view = self.messages
        request = self.factory.post(url, self.data)
        force_authenticate(request, token=self.user_auth)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_patch_message(self):
        message = MessageModel.objects.create(**self.data)
        url, view = self.message
        request = self.factory.patch(f'{url}/{str(message.uuid)}', self.data)
        force_authenticate(request, token=self.user_auth)
        response = view(request, message.uuid)
        self.assertEqual(response.status_code, 202)