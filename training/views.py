from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .models import Block, Cycle, Activity, Segment

class IndexView(TemplateView):
    template_name = 'index.html'


class BlockListView(ListView):
    model = Block
    template_name = 'block_list.html'
    context_object_name = 'blocks'
    ordering = ['-start']


class BlockDetailView(DetailView):
    model = Block
    template_name = 'block_details.html'
    context_object_name = 'current_block'

class CycleListView(ListView):
    model = Cycle
    template_name = 'cycles.html'
    context_object_name = 'cycles'
    ordering = ['-start']


class ActivityListView(ListView):
    model = Activity
    template_name = 'activities.html'
    context_object_name = 'activities'
    ordering = ['-timestamp']