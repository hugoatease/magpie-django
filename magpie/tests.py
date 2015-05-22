from django.test import TestCase
from django.core.urlresolvers import reverse
from models import VPNApplication
import base64

class OAuthScopeTestCase(TestCase):
    fixtures = ['user.json', 'oauth.json']
    client_id = 'PusyUU7hriuatfiRAAbeRwBogGEakXATe0DQ34zs'
    client_secret = 'T5FxPSjsg71QySlGW1eO5FEme18ag0M5sWckOzSAOCIE16XIzT8H5LimriHnksH3AW3WiE2HosG3EyvaxtZuztuzyd9yEwA3S7KNfdRuhyBevVNsLhxeNGtqDN8atWV4'

    url = reverse('token')
    auth = 'Basic ' + base64.b64encode(client_id + ':' + client_secret)

    def test_default_scope(self):
        response = self.client.post(self.url, HTTP_AUTHORIZATION=self.auth, data={
            'grant_type': 'client_credentials'
        })

        self.assertEquals(200, response.status_code)

    def test_service_scope(self):
        response = self.client.post(self.url, HTTP_AUTHORIZATION=self.auth, data={
            'grant_type': 'client_credentials',
            'scope': 'read write service'
        })

        self.assertEquals(200, response.status_code)

    def test_service_scope_prevented(self):
        app = VPNApplication.objects.get(client_id=self.client_id)
        app.service = False
        app.save()

        response = self.client.post(self.url, HTTP_AUTHORIZATION=self.auth, data={
            'grant_type': 'client_credentials',
            'scope': 'read write service'
        })

        self.assertEquals(401, response.status_code)