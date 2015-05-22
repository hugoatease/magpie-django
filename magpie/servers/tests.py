from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from models import Server


class ServerTestCase(TestCase):
    fixtures = ['servers.json']

    def setUp(self):
        User.objects.create_user("test", password="test")

    def login(self):
        self.client.login(username="test", password="test")

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