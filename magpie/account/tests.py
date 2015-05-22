from django.test import TestCase
from django.core.urlresolvers import reverse

class AccountTestCase(TestCase):
    fixtures = ['user.json']
    url = reverse('account_account')

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_account_page(self):
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

    def test_password_change(self):
        response = self.client.post(self.url, {
            'password': 1,
            'old_password': 'admin',
            'new_password1': 'holyfire',
            'new_password1': 'holyfire'
        })
        self.assertEquals(200, response.status_code)

    def test_profile_change(self):
        response = self.client.post(self.url, {
            'profile': 1,
            'first_name': 'Holy',
            'last_name': 'Fire'
        })
        self.assertEquals(200, response.status_code)

    def test_email_change(self):
        response = self.client.post(self.url, {
            'emailchange': 1,
            'email': 'admin@example.com'
        })
        self.assertEquals(200, response.status_code)

        response = self.client.post(self.url, {
            'emailchange': 1,
            'email': 'holy@example.com'
        })
        self.assertEquals(200, response.status_code)

    def test_invite(self):
        response = self.client.post(self.url, {
            'invitechange': 1,
            'email': 'admin@example.com'
        })
        self.assertEquals(200, response.status_code)

        response = self.client.post(self.url, {
            'invitechange': 1,
            'email': 'holy@example.com'
        })
        self.assertEquals(200, response.status_code)