# from django.contrib import admin
from django.urls import path
from account import views
from django.views.generic import RedirectView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.Userlogin, name="login"),
    path('profile/',views.profile, name="profile"),
    path('', RedirectView.as_view(url='home/')),

]