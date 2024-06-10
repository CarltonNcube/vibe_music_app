from django.test import SimpleTestCase
from django.urls import reverse, resolve
from my_app.views import login_view, signup_view, profile_view, music_view, search_view

class UrlsTest(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup_view)

    def test_profile_url_resolves(self):
        url = reverse('profile', args=['username'])
        self.assertEqual(resolve(url).func, profile_view)

    def test_music_url_resolves(self):
        url = reverse('music')
        self.assertEqual(resolve(url).func, music_view)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, search_view)

    def test_invalid_login_url(self):
        with self.assertRaises(NoReverseMatch):
            reverse('login', args=['invalid'])

    def test_invalid_signup_url(self):
        with self.assertRaises(NoReverseMatch):
            reverse('signup', args=['invalid'])

    def test_invalid_profile_url(self):
        with self.assertRaises(NoReverseMatch):
            reverse('profile', args=[])

    def test_invalid_music_url(self):
        with self.assertRaises(NoReverseMatch):
            reverse('music', args=['invalid'])

    def test_invalid_search_url(self):
        with self.assertRaises(NoReverseMatch):
            reverse('search', args=['invalid'])

    def test_login_url_redirect(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_url_redirect(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_profile_url_redirect(self):
        response = self.client.get(reverse('profile', args=['username']))
        self.assertEqual(response.status_code, 200)

    def test_music_url_redirect(self):
        response = self.client.get(reverse('music'))
        self.assertEqual(response.status_code, 200)

    def test_search_url_redirect(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_login_url_method_not_allowed(self):
        response = self.client.post(reverse('login'))
        self.assertEqual(response.status_code, 405)

    def test_signup_url_method_not_allowed(self):
        response = self.client.post(reverse('signup'))
        self.assertEqual(response.status_code, 405)

    def test_profile_url_method_not_allowed(self):
        response = self.client.post(reverse('profile', args=['username']))
        self.assertEqual(response.status_code, 405)

    def test_music_url_method_not_allowed(self):
        response = self.client.post(reverse('music'))
        self.assertEqual(response.status_code, 405)

    def test_search_url_method_not_allowed(self):
        response = self.client.post(reverse('search'))
        self.assertEqual(response.status_code, 405)

