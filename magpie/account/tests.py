from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string
from models import Invite, PasswordRecovery, MailValidation
from django.contrib.auth.models import User


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
            'new_password2': 'holyfire'
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


class SignupTestCase(TestCase):
    fixtures = ['user.json', 'servers.json']

    @override_settings(SELF_REGISTER=True)
    def test_begin(self):
        url = reverse('account_signup_begin')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        response = self.client.post(url, {'email': 'admin@example.com'})
        self.assertEquals(200, response.status_code)

        response = self.client.post(url, {'email': 'holy@example.com'})
        self.assertEquals(200, response.status_code)

    @override_settings(SELF_REGISTER=False)
    def test_begin_disabled(self):
        url = reverse('account_signup_begin')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('account_login'), fetch_redirect_response=False)

    def test_wrong_invite(self):
        url = reverse('account_signup', kwargs={'token': 'foals'})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('account_login'), fetch_redirect_response=False)

    def test_signup(self):
        token = get_random_string(length=50)
        Invite(email='holy@example.com', token=token).save()

        url = reverse('account_signup', kwargs={'token': token})
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        response = self.client.post(url, {
            'username': 'holy',
            'password1': 'fire',
            'password2': 'fire',
            'first_name': 'Holy',
            'last_name': 'Fire'
        })

        self.assertRedirects(response, reverse('index'), fetch_redirect_response=False)


class RecoveryTestCase(TestCase):
    fixtures = ['user.json']

    def test_begin_form(self):
        url = reverse('account_password_recovery_begin')
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_begin_wrong_email(self):
        url = reverse('account_password_recovery_begin')
        response = self.client.post(url, {'email': 'holy@example.com'})
        self.assertEquals(200, response.status_code)

    def test_begin(self):
        url = reverse('account_password_recovery_begin')
        response = self.client.post(url, {'email': 'admin@example.com'})
        self.assertEquals(200, response.status_code)

    def test_recover_wrong_token(self):
        url = reverse('account_password_recovery', kwargs={'token': 'foals'})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('account_login'), fetch_redirect_response=False)

    def test_recover(self):
        user = User.objects.get(username='admin')
        token = get_random_string(length=50)
        PasswordRecovery(user=user, email='admin@example.com', token=token).save()

        url = reverse('account_password_recovery', kwargs={'token': token})
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

        response = self.client.post(url, {
            'new_password1': 'holyfire',
            'new_password2': 'holyfire'
        })
        self.assertEquals(200, response.status_code)


class MailValidationTestCase(TestCase):
    fixtures = ['user.json']

    def test_wrong_token(self):
        url = reverse('account_mailvalidation', kwargs={'token': 'foals'})
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)

    def test_validation(self):
        user = User.objects.get(username='admin')
        token = get_random_string(length=50)
        MailValidation(user=user, token=token, email='holy@example.com').save()

        url = reverse('account_mailvalidation', kwargs={'token': token})
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)