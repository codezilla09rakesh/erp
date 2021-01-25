from django.urls import path
from holiday import views

urlpatterns=[
    path('apply-leave/', views.AddLeave, name="apply_leave"),
    path('list-leave/', views.ListLeaves, name="list_liaves"),
    path('detail-leave/<int:id>', views.ShowLeave, name="detail_leave"),
]