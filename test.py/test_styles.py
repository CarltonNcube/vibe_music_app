from django.test import SimpleTestCase

class CSSFileTests(SimpleTestCase):

    def test_profile_style_exists(self):
        response = self.client.get('/static/css/profile-style.css')
        self.assertEqual(response.status_code, 200)

    def test_search_style_exists(self):
        response = self.client.get('/static/css/search-style.css')
        self.assertEqual(response.status_code, 200)

    def test_style_exists(self):
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)

    def test_profile_style_content(self):
        response = self.client.get('/static/css/profile-style.css')
        self.assertContains(response, 'body {')

    def test_search_style_content(self):
        response = self.client.get('/static/css/search-style.css')
        self.assertContains(response, 'body {')

    def test_style_content(self):
        response = self.client.get('/static/css/style.css')
        self.assertContains(response, 'body {')

    def test_profile_style_missing_class(self):
        response = self.client.get('/static/css/profile-style.css')
        self.assertNotContains(response, '.nonexistent-class')

    def test_search_style_missing_class(self):
        response = self.client.get('/static/css/search-style.css')
        self.assertNotContains(response, '.nonexistent-class')

    def test_style_missing_class(self):
        response = self.client.get('/static/css/style.css')
        self.assertNotContains(response, '.nonexistent-class')

    def test_profile_style_specific_class(self):
        response = self.client.get('/static/css/profile-style.css')
        self.assertContains(response, '.profile-container')

    def test_search_style_specific_class(self):
        response = self.client.get('/static/css/search-style.css')
        self.assertContains(response, '.search-container')

    def test_style_specific_class(self):
        response = self.client.get('/static/css/style.css')
        self.assertContains(response, '.common-class')

    def test_profile_style_syntax_error(self):
        response = self.client.get('/static/css/profile-style.css')
        self.assertNotContains(response, '} {')

    def test_search_style_syntax_error(self):
        response = self.client.get('/static/css/search-style.css')
        self.assertNotContains(response, '} {')

    def test_style_syntax_error(self):
        response = self.client.get('/static/css/style.css')
        self.assertNotContains(response, '} {')

    def test_profile_style_comments(self):
        response = self.client.get('/static/css/profile-style.css')
        self.assertContains(response, '/*')

    def test_search_style_comments(self):
        response = self.client.get('/static/css/search-style.css')
        self.assertContains(response, '/*')

    def test_style_comments(self):
        response = self.client.get('/static/css/style.css')
        self.assertContains(response, '/*')

    def test_profile_style_no_inline_styles(self):
        response = self.client.get('/static/css/profile-style.css')
        self.assertNotContains(response, 'style=')

    def test_search_style_no_inline_styles(self):
        response = self.client.get('/static/css/search-style.css')
        self.assertNotContains(response, 'style=')

    def test_style_no_inline_styles(self):
        response = self.client.get('/static/css/style.css')
        self.assertNotContains(response, 'style=')

