from django.test import TestCase
from .models import Image,Profile

# Create your tests here.
class ProfileTestClass(TestCase):

    """
    Test profile class and its functions
    """
    def setUp(self):

        self.user = User.objects.create(id =1,username='hannah')
        self.profile = Profile(dp='', bio='', contact=" ",user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_method(self):
        """
        Function to test that profile is being saved
        """
        self.profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)

