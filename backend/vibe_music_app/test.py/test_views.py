from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_music_view(self):
        response = self.client.get(reverse('music'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'music.html')

    def test_search_view(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_login_view_with_wrong_password(self):
        response = self.client.post(reverse('login'),
                {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_signup_view_with_existing_username(self):
        User.objects.create_user(username='existinguser', password='password')
        response = self.client.post(reverse('signup'),
                {'username': 'existinguser', 'password1': 'password', 'password2': 'password'})
        self.assertContains(response, 'A user with that username already exists.')

    def test_profile_view_without_login(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 302)

    def test_music_view_without_login(self):
        response = self.client.get(reverse('music'))
        self.assertEqual(response.status_code, 200)

    def test_search_view_without_login(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post(self):
        response = self.client.post(reverse('login'),
                {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

    def test_signup_view_post(self):
        response = self.client.post(reverse('signup'),
                {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 302)

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)

    def test_music_view_get(self):
        response = self.client.get(reverse('music'))
        self.assertEqual(response.status_code, 200)

    def test_search_view_get(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_invalid_method(self):
        response = self.client.put(reverse('login'))
        self.assertEqual(response.status_code, 405)

    def test_signup_view_invalid_method(self):
        response = self.client.put(reverse('signup'))
        self.assertEqual(response.status_code, 405)

    def test_profile_view_invalid_method(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.put(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 405)

    def test_music_view_invalid_method(self):
        response = self.client.put(reverse('music'))
        self.assertEqual(response.status_code, 405)

    def test_search_view_invalid_method(self):
        response = self.client.put(reverse('search'))
        self.assertEqual(response.status_code, 405)

    # API Tests

    def test_api_login(self):
        response = self.client.post(reverse('api_login'),
                {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('username'), 'testuser')

    def test_api_signup(self):
        response = self.client.post(reverse('api_signup'),
                {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('username'), 'newuser')

    def test_api_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('api_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('username'), 'testuser')

    def test_api_music(self):
        response = self.client.get(reverse('api_music'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'success')

    def test_api_search(self):
        response = self.client.get(reverse('api_search'), {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.json())

    # Edge Case Tests

    def test_api_login_invalid_password(self):
        response = self.client.post(reverse('api_login'),
                {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 400)

    def test_api_signup_existing_user(self):
        User.objects.create_user(username='existinguser', password='password')
        response = self.client.post(reverse('api_signup'),
                {'username': 'existinguser', 'password1': 'password', 'password2': 'password'})
        self.assertEqual(response.status_code, 400)

    def test_api_profile_unauthenticated(self):
        response = self.client.get(reverse('api_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 403)

    def test_api_music_unauthenticated(self):
        response = self.client.get(reverse('api_music'))
        self.assertEqual(response.status_code, 200)

    def test_api_search_unauthenticated(self):
        response = self.client.get(reverse('api_search'), {'query': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_api_login_invalid_method(self):
        response = self.client.get(reverse('api_login'))
        self.assertEqual(response.status_code, 405)

    def test_api_signup_invalid_method(self):
        response = self.client.get(reverse('api_signup'))
        self.assertEqual(response.status_code, 405)

    def test_api_profile_invalid_method(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('api_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 405)

    def test_api_music_invalid_method(self):
        response = self.client.post(reverse('api_music'))
        self.assertEqual(response.status_code, 405)

    def test_api_search_invalid_method(self):
        response = self.client.post(reverse('api_search'), {'query': 'test'})
        self.assertEqual(response.status_code, 405)

    def test_api_login_missing_field(self):
        response = self.client.post(reverse('api_login'), {'username': 'testuser'})
        self.assertEqual(response.status_code, 400)

    def test_api_signup_missing_field(self):
        response = self.client.post(reverse('api_signup'),
                {'username': 'newuser', 'password1': 'newpassword'})
        self.assertEqual(response.status_code, 400)

    def test_api_profile_nonexistent_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('api_profile', args=['nonexistentuser']))
        self.assertEqual(response.status_code, 404)

    def test_api_music_no_content(self):
        response = self.client.get(reverse('api_music'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('content')), 0)

    def test_api_search_no_query(self):
        response = self.client.get(reverse('api_search'))
        self.assertEqual(response.status_code, 400)

    def test_api_login_empty_payload(self):
        response = self.client.post(reverse('api_login'), {})
        self.assertEqual(response.status_code, 400)

    def test_api_signup_empty_payload(self):
        response = self.client.post(reverse('api_signup'), {})
        self.assertEqual(response.status_code, 400)

    def test_api_profile_empty_username(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('api_profile', args=['']))
        self.assertEqual(response.status_code, 404)

    def test_api_music_invalid_content(self):
        response = self.client.get(reverse('api_music'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json().get('status'), 'failure')

    def test_api_search_empty_result(self):
        response = self.client.get(reverse('api_search'), {'query': 'nonexistentquery'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().get('results')), 0)

