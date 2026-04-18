from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blocks/', BlockListView.as_view(), name='block-list'),
    path('blocks/<int:pk>/', BlockDetailView.as_view(), name='block-detail'),
    path('cycles/', CycleListView.as_view(), name='cycle-list'),
    path('cycles/<int:pk>/', CycleDetailView.as_view(), name='cycle-detail'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('activities/<int:pk>', ActivityDetailView.as_view(), name='activity-detail'),
]