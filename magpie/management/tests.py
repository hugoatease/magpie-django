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

    def test_access_config(self):
        url = reverse('management_getconfig', kwargs={'name': 'magpie'})
        response = self.client.post(url, {'id': 1})
        self.assertEquals(200, response.status_code)
        self.assertEquals('application/octet-stream', response['Content-Type'])
        self.assertEquals('attachment', response['Content-Disposition'])

    def test_bandwidth_report(self):
        url = reverse('management_bandwidth')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_logs(self):
        url = reverse('management_logs')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_logs_clear(self):
        url = reverse('management_logs')
        response = self.client.post(url, {'clear_history': 1})
        self.assertEquals(200, response.status_code)

    def test_logs_optout(self):
        url = reverse('management_logs')
        response = self.client.post(url, {'optout': 1})
        self.assertEquals(200, response.status_code)

    def test_logs_optin(self):
        url = reverse('management_logs')
        response = self.client.post(url, {'optout': 0})
        self.assertEquals(200, response.status_code)