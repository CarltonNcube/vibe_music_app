from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TemplateTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    # Login template tests with edge cases
    def test_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Log in')

    def test_login_template_with_empty_username(self):
        response = self.client.post(reverse('login'),
                {'username': '', 'password': 'password'})
        self.assertContains(response, 'This field is required.')

    def test_login_template_with_empty_password(self):
        response = self.client.post(reverse('login'),
                {'username': 'testuser', 'password': ''})
        self.assertContains(response, 'This field is required.')

    def test_login_template_with_wrong_password(self):
        response = self.client.post(reverse('login'),
                {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_login_template_with_nonexistent_username(self):
        response = self.client.post(reverse('login'),
                {'username': 'nonexistent', 'password': 'password'})
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_login_template_html_structure(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<form')
        self.assertContains(response, '<input')
        self.assertContains(response, '<button')

    def test_login_template_username_placeholder(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'placeholder="Username"')

    def test_login_template_password_placeholder(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'placeholder="Password"')

    def test_login_template_csrf_token(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_login_template_error_message(self):
        response = self.client.post(reverse('login'),
                {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, 'Please enter a correct username and password.')

    # Signup template tests with edge cases
    def test_signup_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'signup.html')
        self.assertContains(response, 'Signup')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Confirm Password')

    def test_signup_template_with_empty_username(self):
        response = self.client.post(reverse('signup'),
                {'username': '', 'password1': 'password', 'password2': 'password'})
        self.assertContains(response, 'This field is required.')

    def test_signup_template_with_empty_password(self):
        response = self.client.post(reverse('signup'),
                {'username': 'testuser', 'password1': '', 'password2': ''})
        self.assertContains(response, 'This field is required.')

    def test_signup_template_with_password_mismatch(self):
        response = self.client.post(reverse('signup'),
                {'username': 'testuser', 'password1': 'password1', 'password2': 'password2'})
        self.assertContains(response, 'The two password fields didn’t match.')

    def test_signup_template_with_existing_username(self):
        User.objects.create_user(username='testuser2', password='password')
        response = self.client.post(reverse('signup'),
                {'username': 'testuser2', 'password1': 'password', 'password2': 'password'})
        self.assertContains(response, 'A user with that username already exists.')

    def test_signup_template_html_structure(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, '<form')
        self.assertContains(response, '<input')
        self.assertContains(response, '<button')

    def test_signup_template_username_placeholder(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'placeholder="Username"')

    def test_signup_template_password_placeholder(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'placeholder="Password"')

    def test_signup_template_confirm_password_placeholder(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'placeholder="Confirm Password"')

    def test_signup_template_csrf_token(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_signup_template_error_message(self):
        response = self.client.post(reverse('signup'), {'username': '', 'password1': 'password', 'password2': 'password'})
        self.assertContains(response, 'This field is required.')

    # Profile template tests with edge cases
    def test_profile_template(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'Profile')
        self.assertContains(response, self.user.username)

    def test_profile_template_with_nonexistent_user(self):
        response = self.client.get(reverse('profile', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)

    def test_profile_template_html_structure(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, '<h1')
        self.assertContains(response, '<div')
        self.assertContains(response, '<p')

    def test_profile_template_username_display(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, self.user.username)

    def test_profile_template_update_link(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, 'href="/update-profile"')

    def test_profile_template_csrf_token(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_profile_template_bio_display(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, 'Bio')

    def test_profile_template_update_button(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, '<button')

    def test_profile_template_logout_link(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertContains(response, 'href="/logout"')

    def test_profile_template_error_message(self):
        response = self.client.get(reverse('profile', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)

    # Music template tests with edge cases
    def test_music_template(self):
        response = self.client.get(reverse('music'))
        self.assertTemplateUsed(response, 'music.html')
        self.assertContains(response, 'Music')
        self.assertContains(response, 'Top Tracks')

    def test_music_template_html_structure(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, '<h1')
        self.assertContains(response, '<div')
        self.assertContains(response, '<p')

    def test_music_template_with_no_tracks(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, 'No tracks available')

    def test_music_template_track_display(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, 'Track Name')

    def test_music_template_artist_display(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, 'Artist Name')

    def test_music_template_album_display(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, 'Album Name')

    def test_music_template_genre_display(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, 'Genre')

    def test_music_template_duration_display(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, 'Duration')

    def test_music_template_play_button(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, '<button')

    def test_music_template_error_message(self):
        response = self.client.get(reverse('music'))
        self.assertContains(response, 'No tracks available')

    # Search template tests with edge cases
    def test_search_template(self):
        response = self.client.get(reverse('search'))
        self.assertTemplateUsed(response, 'search.html')
        self.assertContains(response, 'Search')
        self.assertContains(response, 'Results')

    def test_search_template_html_structure(self):
        response = self.client.get(reverse('search'))
        self.assertContains(response, '<form')
        self.assertContains(response, '<input')
        self.assertContains(response, '<button')

    def test_search_template_with_empty_query(self):
        response = self.client.post(reverse('search'), {'query': ''})
        self.assertContains(response, 'This field is required.')

    def test_search_template_with_no_results(self):
        response = self.client.post(reverse('search'), {'query': 'nonexistent'})
        self.assertContains(response, 'No results found')

    def test_search_template_with_results(self):
        # Assume there's a search result with the term 'test'
        response = self.client.post(reverse('search'), {'query': 'test'})
        self.assertContains(response, 'test result')

    def test_search_template_query_display(self):
        response = self.client.post(reverse('search'), {'query': 'test'})
        self.assertContains(response, 'Search Results for "test"')

    def test_search_template_result_count(self):
        response = self.client.post(reverse('search'), {'query': 'test'})
        self.assertContains(response, '1 result found')

    def test_search_template_result_item(self):
        response = self.client.post(reverse('search'), {'query': 'test'})
        self.assertContains(response, 'test result item')

    def test_search_template_result_link(self):
        response = self.client.post(reverse('search'), {'query': 'test'})
        self.assertContains(response, 'href="/result/test"')

    def test_search_template_csrf_token(self):
        response = self.client.get(reverse('search'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_search_template_error_message(self):
        response = self.client.post(reverse('search'), {'query': ''})
        self.assertContains(response, 'This field is required.')

