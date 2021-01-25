from django.urls import path
from holiday import views

urlpatterns=[
    path('apply-leave/', views.Leave, name="leave"),
]