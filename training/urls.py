from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('blocks/', BlockListView.as_view(), name='block-list'),
    path('blocks/<int:pk>/', BlockDetailView.as_view(), name='block-detail'),
    path('cycles/', CycleListView.as_view(), name='cycle-list'),
]