from .base import BaseTest
from posthog.models import User

class TestUser(BaseTest):
    TESTS_API = True
    def test_redirect_to_site(self):
        self.team.app_url = 'http://somewebsite.com'
        self.team.save()
        response = self.client.get('/api/user/redirect_to_site/?actionId=1')
        self.assertIn('http://somewebsite.com', response.url)

    def test_create_user_when_restricted(self):
        with self.settings(RESTRICT_SIGNUPS='posthog.com,uk.posthog.com'):
            with self.assertRaisesMessage(ValueError, "Can't sign up with this email"):
                User.objects.create_user(email='tim@gmail.com')

            user = User.objects.create_user(email='tim@uk.posthog.com')
            self.assertEqual(user.email, 'tim@uk.posthog.com')

    def test_create_user_with_distinct_id(self):
        with self.settings(TEST=False):
            user = User.objects.create_user(email='tim@gmail.com')
        self.assertNotEqual(user.distinct_id, '')
        self.assertNotEqual(user.distinct_id, None)

class TestLoginViews(BaseTest):
    def test_redirect_to_setup_admin_when_no_users(self):
        User.objects.all().delete()
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/setup_admin')