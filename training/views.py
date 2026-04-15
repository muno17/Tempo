from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Block, Cycle, Activity, Segment

class IndexView(TemplateView):
    template_name = "index.html"


class ActivityListView(ListView):
    model = Activity
    template_name = "activities.html"
    context_object_name = "activities"
    ordering = ["-timestamp"]