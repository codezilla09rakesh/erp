from django.urls import path
from holiday import views

urlpatterns=[
    path('apply-leave/', views.AddLeave, name="apply_leave"),
    path('list-leave/', views.ListLeaves, name="list_liaves"),
    path('detail-leave/<int:id>', views.ShowLeave, name="detail_leave"),
    path('approved-leave/<int:id>/<str:val>/', views.ApprovedLeave, name="approved_leave"),
    path('resion/<int:id>', views.ResionView, name="resion"),
    path('resion-show/<int:id>', views.ResionShow, name="resion_show"),
]