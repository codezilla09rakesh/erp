from oauthlib.oauth2 import BearerToken
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory, APIClient
from oauth2_provider.models import AccessToken
from django.test import Client
from django.urls import reverse
from account.models import CustomUser
from apiApp.views import Token, RevokeToken, UserLeave, UserProfile, AddEmployee, RemoveEmployee, ApprovedLeave
from apiApp.serializer import UserSerializer
from rest_framework import status
import requests
from erp import settings
from holiday.models import YourEmployee, Leave
# from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import authenticate
from apiApp.serializer import UserSerializer
import json
from datetime import date

# Create your tests here.

class ApiTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.super=CustomUser.objects.create_superuser(username="admin1", password="admin")
        self.user=CustomUser.objects.create_user(username="rakesh@gmail.com", password="123456", is_manager=True)
        # manager = CustomUser.objects.filter(is_superuser=True)[0]
        YourEmployee.objects.create(manager=self.super, employee=self.user)
        self.r = requests.post(settings.URL_TYPE + "/o/token/",
                          data={
                              "grant_type": "password",
                              "username": "rakesh@gmail.com",
                              "password": "123456",
                              "client_id": settings.CLIENT_ID,
                              "client_secret": settings.CLIENT_SECRET
                          })
        user = CustomUser.objects.create_superuser(username="admin", password="admin")

        # apply for leave
        # data = {
        #     "title": "test leave",
        #     "description": "sdfdsfdss",
        #     "starting_date": "2021-01-29",
        #     "ending_date": "2021-01-30",
        #     "half_day": "select ",
        #     "status": "panding"}
        # request = self.factory.post(reverse("leaveapi"),data, format="json")
        # print('request', request)
        # force_authenticate(request,user=user, token=self.r.json()['access_token'])

        for i in range(10):
            manager= False
            if i%2==0:
                manager = True
            username = "rakesh"+str(i)+"@gmail.com"
            CustomUser.objects.create_user(username=username, first_name = "rakesh", last_name = "singh", password = "123456", is_manager = manager )

    # def test_user_list(self):
    #     # print('reverse', reverse('userlistapi'))
    #     # print('reverse', reverse('userlistapi'))
    #     respones = self.client.get(reverse('userlistapi'))
    #     user = CustomUser.objects.all()
    #     serializer = UserSerializer(user, many=True)
    #     self.assertEqual(respones.data, serializer.data)
    #     self.assertEqual(respones.status_code, status.HTTP_200_OK)
    #
    # def test_manager_list(self):
    #     respones = self.client.get(reverse('manager_list'))
    #     user = CustomUser.objects.filter(is_manager=True)
    #     serializer = UserSerializer(user, many=True)
    #     self.assertEqual(respones.data, serializer.data)
    #     self.assertEqual(respones.status_code, status.HTTP_200_OK)

    # def test_post_registration(self):
    #     data = {
    #         "username":"rakesh21@gmail.com",
    #         "password":"123456",
    #         "first_name":"rakesh",
    #         "last_name":"Singh",
    #         "email":"rakesh21@gmail.com",
    #         "is_manager":True
    #     }
    #     response = self.client.post(reverse('register'), data=data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_anonymous_cannot_see_contacts(self):
    #     factory = APIRequestFactory()
    #     user = CustomUser.objects.get(username='admin')
    #     view = Token.as_view()
    #
    #     # Make an authenticated request to the view...
    #     request = factory.post(reverse('token'),{"username":"admin","password":"admin"})
    #     force_authenticate(request, user=user)
    #     response = view(request)
        # print(response)
    #     response = self.client.get(reverse("login"))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_post_login(self):
    #     c = Client(enforce_csrf_checks=False)
    #     response = c.post(reverse('token'), {"username":"admin", "password":"admin"})
    #
    #     r = requests.post(settings.URL_TYPE + "/o/token/",
    #                       data={
    #                           "grant_type": "password",
    #                           "username": "rakesh@gmail.com",
    #                           "password": "123456",
    #                           "client_id": settings.CLIENT_ID,
    #                           "client_secret": settings.CLIENT_SECRET,
    #                       },
    #                       )
    #     # print('requests', r.json()['access_token'])
    #     self.assertEqual(response.status_code, r.status_code)

    # def test_see_all_leave(self):
    #     factory=self.factory
    #     view = UserLeave.as_view()
    #     user = CustomUser.objects.get(username = "rakesh@gmail.com")
    #     request = factory.get(reverse('leaveapi'),{"token":self.r.json()['access_token']})
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     # print('response',response)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_apply_for_leave(self):
    #     factory = self.factory
    #     view = UserLeave.as_view()
    #     user =CustomUser.objects.get(username="rakesh@gmail.com")
    #     data = {
    #         "title": "test leave",
    #         "description": "sdfdsfdss",
    #         "starting_date": "2021-01-29",
    #         "ending_date": "2021-01-30",
    #         "half_day": "select ",
    #         "status": "panding"}
    #     # data = json.dumps(data)
    #     # print('data',data)
    #     request = factory.post(reverse("leaveapi"), data, format="json")
    #     force_authenticate(request,user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create_profile(self):
    #     factory = self.factory
    #     view = UserProfile.as_view()
    #     user = CustomUser.objects.get(username = "rakesh@gmail.com")
    #     data={
    #         "user":user.id,
    #         "mobile":"3214569873",
    #         "gender":"male"
    #     }
    #     request = factory.post(reverse('profileapi'), data, format="json")
    #     print('request',request, reverse('profileapi'))
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     print('response',response)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # def test_profile_read(self):
    #     factory = self.factory
    #     view = UserProfile.as_view()
    #     user = CustomUser.objects.get(username="rakesh@gmail.com")
    #     request = factory.get(reverse('profileapi'))
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #

    # def test_manager_employee(self):
    #     factory = self.factory
    #     view = AddEmployee.as_view()
    #     user = CustomUser.objects.get(username = "rakesh@gmail.com")
    #     request = factory.get(reverse('addemployeeapi'))
    #     # print('request',request, reverse('addemployeeapi'))
    #     force_authenticate(request, user=user)
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_add_employee(self):
    #     factory = self.factory
    #     view = AddEmployee.as_view()
    #     user = CustomUser.objects.get(username = "rakesh@gmail.com")
    #     non_manager_user = CustomUser.objects.filter(is_manager=False)
    #     serailzer = UserSerializer(non_manager_user,many=True)
    #     data = serailzer.data
    #     request = factory.post(reverse('addemployeeapi'), data, format="json")
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_get_remove_employee(self):
    #     factory = self.factory
    #     view = RemoveEmployee.as_view()
    #     user = CustomUser.objects.get(username = "rakesh@gmail.com")
    #     request = factory.get(reverse("removeemployeeapi"))
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_post_remove_employee(self):
    #     factory = self.factory
    #     view = RemoveEmployee.as_view()
    #     user = CustomUser.objects.get(username = "rakesh@gmail.com")
    #     manager_employee = YourEmployee.objects.filter(manager=user)
    #     serializer = UserSerializer(manager_employee, many=True)
    #     data = serializer.data
    #     request = factory.post(reverse("removeemployeeapi"),data, format="json")
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_get_approved(self):
    #     factory = self.factory
    #     view = ApprovedLeave.as_view()
    #     user = CustomUser.objects.get(username = "rakesh@gmail.com")
    #     request = factory.get(reverse("approvedleaveapi"))
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     Leave.objects.create(manager=self.super, employee=self.user,
    #                          title = "This is title", description=";adslkfja;kdf",
    #                          starting_date=date.today(), half_day="first_day")
    #     leave = Leave.objects.all()
    #     print('leave', leave)
    #     response = view(request)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_logout(self):
    #     factory=self.factory
    #     view = RevokeToken.as_view()
    #     user = CustomUser.objects.get(username ="rakesh0@gmail.com")
    #     # Make an authenticated request to the view...
    #     request = factory.post(reverse('logoutapi'),{"token":self.r.json()['access_token']})
    #     # print('request', request)
    #     force_authenticate(request, user=user, token=self.r.json()['access_token'])
    #     response = view(request)
    #     # client = APIClient()
    #     # client.force_authenticate(user=user, )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

