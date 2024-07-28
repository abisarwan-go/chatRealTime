from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.NotificationsView.as_view(), name='notifications'),

]