from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posting.models import BlogPost
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER
# automated
# new / blank db

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj =User(username='testcfeuser', email='test@test.com')
        user_obj.set_password("somerandompassword")
        user_obj.save()
        blog_post = BlogPost.objects.create(user=user_obj, title='New title', content='somerandomcontent')

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = User.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse("api_posting:post_listcreate")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_post_list(self):
        data = {"title": "Some random title", "content": "some more content"}
        url = api_reverse("api_posting:post_listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORISED)


    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {"title": "Some random title", "content": "some more content"}
        url = blog_post.get_api_url()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        blog_post =BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {"title": "Some random title", "content": "some more content"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_UNAUTHORISED)


        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORISED)

    def test_update_item_wih_user(self):
        blog_post =BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {"title": "Some random title", "content": "some more content"}
        user_obj =User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT' + token_rsp)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list(self):

        user_obj =User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        data = {"title": "Some random title", "content": "some more content"}
        url = api_reverse("api_posting:post_listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_2011_CREATED)

    def test_user_ownership(self):

        owner =User.objects.create(username='testuser22')
        blog_post = BlogPost.objects.create(user=owner, title='New title', content='somerandomcontent')
        user_obj =User.objects.first()
        self.assertNotEqual(user_obj)
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        data = {"title": "Some random title", "content": "some more content"}
        url = api_reverse("api_posting:post_listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_2011_CREATED)


# Below test is not properly written
    def test_user_login(self):
        data = {
            'username': 'testcfeuser',
            'password': 'somerandompassword'
        }
        url = api_reverse("api_login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            blog_post = BlogPost.objects.first()


            data = {"title": "Some random title", "content": "some more content"}
            self.client.credentials(HTTP_AUTHORIZATION='JWT' + token)
            url = api_reverse("api_posting:post_listcreate")
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)




