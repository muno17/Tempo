from django.urls import path
from .views import ActivityListView, TemplateView, IndexView, BlockListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('blocks/', BlockListView.as_view(), name='block-list'),
]