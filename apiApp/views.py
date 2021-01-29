from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from account.models import CustomUser
from apiApp.serializers import UserListSerializer
from apiApp.serializerForm import Register
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.

class UserList(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    #
    # def list(self, request, format=None):
    #     user = CustomUser.objects.all()
    #     # print(self.serializer_class)
    #     serializer = UserListSerializer(user, many=True)
    #     data = serializer.data
    #     return Response(data)



# class CreateUser(APIView):
#     def get(self):
#         pass
#
#     def post(self):
#         pass


# def UserList(request):
#     user = CustomUser.objects.all()
#     serializer = UserListSerializer(user, many=True)
#     data = serializer.data
#     print('Form ',Register())
#     form = Register()
#     return HttpResponse(form)
#     return JsonResponse(data, safe=False)


