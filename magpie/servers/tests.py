from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from models import Server
from magpie.models import VPNApplication


class ServerTestCase(TestCase):
    fixtures = ['user.json', 'servers.json']

    def login(self):
        self.client.login(username="admin", password="admin")

    def test_list(self):
        url = reverse('servers_servers')

        response = self.client.get(url)
        self.assertEquals(302, response.status_code)

        self.login()
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_entry(self):
        url = reverse('servers_server', kwargs={'name': 'magpie'})

        response = self.client.get(url)
        self.assertEquals(302, response.status_code)

        self.login()
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        self.assertContains(response, reverse('servers_config', kwargs={'name': 'magpie'}))
        self.assertContains(response, reverse('servers_authority', kwargs={'name': 'magpie'}))

    def test_servers_config(self):
        url = reverse('servers_config', kwargs={'name': 'magpie'})
        response = self.client.get(url)
        self.assertEquals(302, response.status_code)

        self.login()
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        server = Server.objects.get(name='magpie')
        self.assertEquals(render_to_string('servers/config.ovpn', {'server': server}), response.content)

    def test_servers_authority(self):
        url = reverse('servers_authority', kwargs={'name': 'magpie'})
        response = self.client.get(url)
        self.assertEquals(302, response.status_code)

        self.login()
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        server = Server.objects.get(name='magpie')
        self.assertEquals(render_to_string('servers/ca.pem', {'server': server}), response.content)


class BackendAPITestCase(APITestCase):
    fixtures = ['user.json', 'oauth.json', 'oauth_tokens.json', 'servers.json', 'management.json']

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer QNj05qG3Y1WXUkntMg0kQXOjCYdaa2')

    def test_connect(self):
        url = reverse('server-connect', kwargs={'name': 'magpie'})
        response = self.client.post(url, {
            'username': 'admin',
            'token': 'ZTU3pXIOJMTuWatX0amX',
            'origin': '8.8.8.8'
        })

        self.assertEquals(200, response.status_code)
        self.assertJSONEqual(response.content, {"mask": "255.255.0.0", "type": "TUN", "address": "10.8.0.9"})

    def test_connect_wrong_user(self):
        url = reverse('server-connect', kwargs={'name': 'magpie'})
        response = self.client.post(url, {
            'username': 'foals',
            'token': 'ZTU3pXIOJMTuWatX0amX',
            'origin': '8.8.8.8'
        })

        self.assertEquals(400, response.status_code)

    def test_connect_wrong_token(self):
        url = reverse('server-connect', kwargs={'name': 'magpie'})
        response = self.client.post(url, {
            'username': 'admin',
            'token': 'wrongtoken',
            'origin': '8.8.8.8'
        })

        self.assertEquals(403, response.status_code)

    def test_disconnect(self):
        url = reverse('server-disconnect', kwargs={'name': 'magpie'})
        response = self.client.post(url, {
            'username': 'admin',
            'address': '10.8.0.9',
            'received': 1000,
            'sent': 1000
        })

        self.assertEquals(202, response.status_code)

    def test_disconnect_wrong_username(self):
        url = reverse('server-disconnect', kwargs={'name': 'magpie'})
        response = self.client.post(url, {
            'username': 'foals',
            'address': '10.8.0.9',
            'received': 1000,
            'sent': 1000
        })

        self.assertEquals(400, response.status_code)