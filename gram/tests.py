from django.test import TestCase
from .models import Image,Profile,Comments

# Create your tests here.
class ProfileTestClass(TestCase):

    """
    Test profile class and its functions
    """
    def setUp(self):

        self.user = User.objects.create(id =1,username='maureen')
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

    def test_delete_method(self):
        """
        Function to test that a profile can be deleted
        """
        self.profile.save_profile()

    def test_update_method(self):
        """
        Function to test that a profile's details can be updated
        """
        self.profile.save_profile()
        new_profile = Profile.objects.filter(bio='').update(bio='')

    
    def test_get_profile_by_id(self):
        """
        Function to test if you can get a profile by its id
        """
        self.profile.save_profile()
        this_pro= self.profile.get_by_id(self.profile.user_id)
        profile = Profile.objects.get(user_id=self.profile.user_id)
        self.assertTrue(this_pro, profile)


class CommentTestClass(TestCase):
    #set up method
    def setUp(self):
        self.comments = Comments(description = 'comment')

     #testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.comments,Comments))

    #testing for saving method
    def test_save_method(self):
        self.comments.save_comment()
        comments = Comments.objects.all()
        self.assertTrue(len(comments) > 0)

    #testing for deleting method
    def test_delete_method(self):
        self.comments.save_comment()
        self.comments.delete_comment()
        comments = Comments.objects.all()
        self.assertTrue(len(comments) == 1 )

class ImageTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.image = Image(image = 'fashion')
    
    def test_instance(self):
        self.assertTrue(isinstance(self.image, Image))

    def tearDown(self):
        self.image.delete_image()
        self.profile.delete_profile()

    def test_save_method(self):
        self.image.save_image()
        images  = Image.objects.all()
        self.assertTrue(len(images)>0)

        

