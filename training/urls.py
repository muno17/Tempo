from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blocks/', BlockListView.as_view(), name='block-list'),
    path('blocks/<int:pk>/', BlockDetailView.as_view(), name='block-detail'),
    path('block_form/', BlockCreateView.as_view(), name='block-create'),
    path('block_delete/<int:pk>', BlockDeleteView.as_view(), name='block-delete'),
    path('block_update/<int:pk>', BlockUpdateView.as_view(), name='block-update'),
    path('cycles/', CycleListView.as_view(), name='cycle-list'),
    path('cycles/<int:pk>/', CycleDetailView.as_view(), name='cycle-detail'),
    path('cycle_form/', CycleCreateView.as_view(), name='cycle-create'),
    path('cycle_form/<int:block_id>/', CycleCreateView.as_view(), name='cycle-create'),
    path('cycle_delete/<int:pk>/', CycleDeleteView.as_view(), name='cycle-delete'),
    path('cycle_update/<int:pk>/', CycleUpdateView.as_view(), name='cycle-update'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('activities/<int:pk>', ActivityDetailView.as_view(), name='activity-detail'),
    path('activity_form/', ActivityCreateView.as_view(), name='activity-create'),
    path('activity_form/<int:cycle_id>/', ActivityCreateView.as_view(), name='activity-create'),
    path('activity_delete/<int:pk>', ActivityDeleteView.as_view(), name='activity-delete'),
    path('activity_update/<int:pk>', ActivityUpdateView.as_view(), name='activity-update'),
]