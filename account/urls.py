# from django.contrib import admin
from django.urls import path
from account import views
from django.views.generic import RedirectView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.Userlogin, name="login"),
    path('profile/', views.Profile, name="profile"),
    path('add-profile/', views.Addprofile, name="add_profile"),
    path('edit-profile/', views.Editprofile, name="edit_profile"),
    path('logout/', views.Userlogout, name="logout"),
    path('add-employee/', views.AddEmployee, name="add_employee"),
    path('remove-employee/', views.RemoveEmployee, name="remove_employee"),
    path('', RedirectView.as_view(url='login/')),

]