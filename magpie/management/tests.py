from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

class ManagementTestCase(TestCase):
    fixtures = ['user.json', 'servers.json', 'management.json']

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_access_list(self):
        url = reverse('management_access')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_access_create(self):
        url = reverse('management_access')
        response = self.client.post(url, {'server': 1})
        self.assertEquals(200, response.status_code)

    def test_access_delete(self):
        url = reverse('management_access')
        response = self.client.post(url, {'id': 1})
        self.assertEquals(200, response.status_code)