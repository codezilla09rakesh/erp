from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import re
from django.shortcuts import redirect
from rest_framework.authtoken.views import ObtainAuthToken

from apiApp.serializer import UserSerializer, RegisterSerializer, ProfileSerializer, LeaveSerializer, LoginAuthSerializer, ResionsSerializer, AcceptSerializer
from account.models import CustomUser, MyProfile
from holiday.models import YourEmployee, Resions
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from holiday.models import Leave
from apiApp.customPermission import CheckManager
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from erp import settings



class UserList(ListModelMixin, GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)

class ManagerList(ListModelMixin, GenericAPIView):
    queryset = CustomUser.objects.filter(is_manager = True)
    serializer_class =UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)

@method_decorator(csrf_exempt, name='dispatch')
class UserRegister(CreateModelMixin, GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class UserLogin(APIView):
#     authentication_classes = [OAuth2Authentication]
#     # def get(self):
#     #     return Response(status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         try:
#             data = request.data
#             serialzer = LoginSerializer(data)
#             if serialzer.is_valid():
#                 # user = serialzer.validated_data['username']
#                 # password = serialzer.validated_data['password']
#                 r = requests.post(
#                     settings.URL_TYPE+"/o/token/",
#                     data={
#                         "grant_type": "password",
#                         "username": data['username'],
#                         "password": data["password"],
#                         "client_id": settings.CLIENT_ID,
#                         "client_secret": settings.CLIENT_SECRET,
#                         # "scope": "admin",
#                     },
#                     verify=False,
#                 )
#         except Exception as e:
#             return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#         # try:
#         #     username = request.data['username']
#         #     password = request.data['password']
#         #     user = authenticate(username=username, password=password)
#         #     if user is not None:
#         #         if user.is_active:
#         #             login(request, user)
#         #             success = {'login':'SuccessFully Login '}
#         #             return Response(success, status=status.HTTP_200_OK)
#         #         else:
#         #             return Response(data={},status=status.HTTP_404_NOT_FOUND)
#         #     else:
#         #         return Response(status=status.HTTP_404_NOT_FOUND)
#         # except Exception as e:
#         #     return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Token(ObtainAuthToken, GenericAPIView):
    permission_classes = []
    serializer_class = LoginAuthSerializer
    def post(self, request, *args, **kwargs):
        """
        Gets tokens with username/email and password. Input should be in the format:
        {"username": "username", "password": "1234abcd"} or
        {"username": "test@email.com", "password": "1234abcd"}
        """
        try:
            print(request.data["username"])
            # check username is email type or not
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
            if re.search(regex, request.data["username"]):
                user = CustomUser.objects.filter(username=request.data["username"])
                if len(user):
                    username = user[0].username
                    # isVerified = user[0].isVerified
                    # scope = user[0].role
                    if user[0].is_active == False:
                        return Response({
                            "message": "Your account has been suspended, please contact customer care service for more information."})
                    # elif isVerified == False:
                    #     return Response({"message": "Email not verified."})
                else:
                    return Response(data={"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = CustomUser.objects.get(username=request.data["username"])
                username = request.data["username"]
                # isVerified = user.isVerified
                # scope = user.role
                if user.is_active == False:
                    return Response({
                        "message": "Your account has been suspended, please contact customer care service for more information."})
                # elif isVerified == False:
                #     return Response({"message": "Email not verified."})
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})
        print("fgdlkdflkgjdflkjglkdfj")
        r = requests.post(settings.URL_TYPE + "/o/token/",
                          data={
                              "grant_type": "password",
                              "username": username,
                              "password": request.data["password"],
                              # "scope": scope,
                              "client_id": settings.CLIENT_ID,
                              "client_secret": settings.CLIENT_SECRET,
                          },
                          )
        if r.status_code == 400:
            json_res = {"message": "Bad request or Invalid credentials"}
            return Response(data=json_res, status=r.status_code)
        else:
            return Response(r.json())


class RefreshToken(APIView):
    permission_classes = []
    def post(self, request):
        """
        Registers user to the server. Input should be in the format:
        {"refresh_token": "<token>"}
        """
        print(request.data["refresh_token"])
        r = requests.post(
            settings.URL_TYPE + "/o/token/",
            data={
                "grant_type": "refresh_token",
                "refresh_token": request.data["refresh_token"],
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },
            verify=False,
        )
        if r.status_code == 200:
            return Response(r.json())
        else:
            return Response(r.json(), r.status_code)

class RevokeToken(APIView):
    """
    Method to revoke tokens.
    {"token": "<token>"}
    """
    def post(self, request):
        print('######################################################')
        r = requests.post(
            settings.URL_TYPE + "/o/revoke_token/",
            data={
                "token": request.data["token"],
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },)
        # If it goes well return success message (would be empty otherwise)
        if r.status_code == requests.codes.ok:
            return Response({"message": "token revoked"}, r.status_code)
        # Return the error if it goes badly
        return Response(r.json(), r.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(username=request.user)
            profile = MyProfile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            data = serializer.data

            return Response(data=data, status=status.HTTP_200_OK)
        except MyProfile.DoesNotExist:
            res = {"profile":"Does Not Exist"}
            # json_data = json.dumps(res)
            return Response(res, status=status.HTTP_404_NOT_FOUND)




@method_decorator(csrf_exempt, name='dispatch')
class UserLogOut(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logout(request)
        data = {"success":"SuccessFully LogOut"}
        return Response(data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserLeave(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [OAuth2Authentication]

    def get_user(self, request):
        user = CustomUser.objects.get(username=request.user)
        return user


    def get(self, request, *args, **kwargs):
        user = self.get_user(request)
        try:
            leave = Leave.objects.filter(employee=user)
            serializer = LeaveSerializer(leave, many=True)
            data = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)
        except Leave.DoesNotExist:
            res = {"leave":"Leave does not exist"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        print("TTTTTTTtttFFFFFFFFFFFFFFFFFFFFFffffffffffffffffffffffff")
        user = self.get_user(request)
        manager = YourEmployee.objects.get(employee=user)
        # user = CustomUser.objects.get(id=manager.manager.id)
        data = request.data
        data['employee']= user.id
        data['manager'] = manager.id
        serializer = LeaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            res ={'success':"Leave applyed"}
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class AddEmployee(APIView):
    permission_classes = [IsAuthenticated, CheckManager]

    def get_user(self, request):
        user = CustomUser.objects.get(username=request.user)
        return user

    def get(self, request, *args, **kwargs):
        user = self.get_user(request)
        youremployee = YourEmployee.objects.filter(manager = user)
        l = []
        for emp in youremployee:
            print(type(emp.employee))
            l.append(emp.employee)
        serializer = UserSerializer(l, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = self.get_user(request)
        data = request.data
        for i in data['employee']:
            employee_user = CustomUser.objects.get(id=i)
            YourEmployee.objects.create(manager=user, employee=employee_user)
        else:
            res = {"success": "Add"}
            return Response(res, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class RemoveEmployee(APIView):
    permission_classes = [IsAuthenticated, CheckManager]

    def get_user(self, request):
        user = CustomUser.objects.get(username=request.user)
        return user

    def get(self, request, *args, **kwargs):
        user = self.get_user(request)
        youremployee = YourEmployee.objects.filter(manager = user)
        l = []
        for emp in youremployee:
            print(type(emp.employee))
            l.append(emp.employee)
        serializer = UserSerializer(l, many=True)
        data = serializer.data
        # data = {}
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = self.get_user(request)
        data = request.data
        for i in data['employee']:
            YourEmployee.objects.get(employee = i).delete()
        else:
            res = {"success":"Delete"}
            return Response(res,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ApprovedLeave(APIView):
    permission_classes = [IsAuthenticated, CheckManager]

    def get_user(self, request):
        user = CustomUser.objects.get(username=request.user)
        return user

    def get(self, request, *args, **kwargs):
        user = self.get_user(request)
        leave = Leave.objects.filter(manager=user, status="panding")
        serializer = LeaveSerializer(leave, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, pk=None,*args, **kwargs):
        leave = Leave.objects.get(pk = pk)
        # if request.data['status'].strip(" ").lower() == "region":
        #     status = request.data['status'].strip(" ").lower()

        serialzer = AcceptSerializer(leave, data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            res = {"success":"Update"}
            return Response(res, status=status.HTTP_200_OK)
        # if status == "region":
        #     print('in side of resion api')
        #     return redirect("addresionapi", pk)
        else:
            return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class AddResion(APIView):
    permission_classes = [IsAuthenticated, CheckManager]

    def get_user(self, request):
        user = CustomUser.objects.get(username=request.user)
        return user

    def post(self, request, id=None):
        leave = Leave.objects.get(id=id)
        print('leave', leave)
        employee = leave.employee
        data = request.data
        data['employee'] = employee
        data['leave'] = leave
        serializer = ResionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            res = {"success":"Resion send"}
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(username = request.user)
        resion_list = Resions.objects.filter(employee = user)
        serializer = ResionsSerializer(resion_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)