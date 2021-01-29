from django.urls import path,include
from apiApp import views
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('user-list/', views.UserList.as_view({'get':'list'}), basename="user-list")
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('v1/', include('rest_framework.urls'), namespace='rest_framework'),
# ]

urlpatterns = [
    path('user-list/', views.UserList.as_view({'get':'list'}), name="list")

]
