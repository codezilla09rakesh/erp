from django.urls import path
from apiApp import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('userlist/', views.UserList.as_view(), name="apihome"),
    path('managerlist/', views.ManagerList.as_view(), name="manager_list"),
    path('register/', views.UserRegister.as_view(), name="register"),
    path('login/', views.Token.as_view(), name='token'),
    path('token-refresh/',views.RefreshToken.as_view(), name="token_refresh"),
    path('logout/', views.RevokeToken.as_view(), name="logoutapi"),
    # path('news/', views.NewsPostView.as_view(), name="news"),
    # path('profile/<int:pk>', views.UserProfile.as_view(), name="profileapi"),
    path('profile/', views.UserProfile.as_view(), name="profileapi"),
    path('logout/', views.UserLogOut.as_view(), name="logoutapi"),

    path('leave/', views.UserLeave.as_view(), name="leaveapi"),
    path('resion/<int:id>/', views.AddResion.as_view(), name='resionapi'),

    path('add-employee/', views.AddEmployee.as_view(), name="addemployeeapi"),
    path('remove-employee/', views.RemoveEmployee.as_view(), name="removeemployeeapi"),

    path('approved-leave/', views.ApprovedLeave.as_view(), name="approvedleaveapi"),
    path('approved-leave/<int:pk>/', views.ApprovedLeave.as_view(), name="approvedleaveapi"),

    path('resion/<int:pk>/', views.AddResion.as_view(), name="addresionapi"),
    path('resion/', views.ResionList.as_view(), name = "resionlistapi"),

]