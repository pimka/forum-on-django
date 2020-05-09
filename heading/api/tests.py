import uuid

from django.urls import reverse
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

from .models import HeadingModel, TagModel
from .views import HeadingAdvancedOperations, HeadingBaseOperations, TagAdvancedOperations, TagBaseOperations


class TagsTestCase(APITestCase):
    def setUp(self):
        self.tags = 'tags', TagBaseOperations.as_view()
        self.tag = 'tag', TagAdvancedOperations.as_view()
        self.factory = APIRequestFactory()
        self.user_uuid = uuid.uuid4()
        self.user_auth = {'uuid': str(
            self.user_uuid), 'username': 'username', 'token': 'token', 'is_staff': True}
        self.data = {'name': 'meh'}

    def test_post_tag(self):
        url, view = self.tags
        request = self.factory.post(url, self.data)
        force_authenticate(request, token=self.user_auth)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_patch_tag(self):
        tag = TagModel.objects.create(**self.data)
        url, view = self.tag
        request = self.factory.patch(f'{url}/{str(tag.uuid)}', self.data)
        force_authenticate(request, token=self.user_auth)
        response = view(request, tag.uuid)
        self.assertEqual(response.status_code, 202)


class HeadingsTestCase(APITestCase):
    def setUp(self):
        self.headings = 'headings_add', HeadingBaseOperations.as_view()
        self.heading = 'heading', HeadingAdvancedOperations.as_view()
        self.factory = APIRequestFactory()
        self.user_uuid = uuid.uuid4()
        self.test_tag = TagModel.objects.all()
        self.user_auth = {'uuid': str(
            self.user_uuid), 'username': 'username', 'token': 'token', 'is_staff': True}
        self.data = {'user_uuid': self.user_uuid, 'header': 'Doge',
                     'body': 'Yellow dog', 'tags': self.test_tag}

    def test_post_heading(self):
        url, view = self.headings
        request = self.factory.post(url, self.data)
        force_authenticate(request, token=self.user_auth)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_patch_heading(self):
        copy = self.data.copy()
        copy.pop('tags')
        head = HeadingModel.objects.create(**copy)
        url, view = self.heading
        request = self.factory.patch(f'{url}/{str(head.uuid)}', self.data)
        force_authenticate(request, token=self.user_auth)
        response = view(request, head.uuid)
        self.assertEqual(response.status_code, 202)
