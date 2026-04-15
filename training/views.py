from django.shortcuts import render
from django.views.generic import ListView
from .models import Block, Cycle, Activity, Segment

def ActivityListView(request):
    model = Activity
    template_name = "activities.html"
    context_object_name = "activities"
    ordering = ["-timestamp"]