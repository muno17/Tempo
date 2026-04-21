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

class CycleDetailView(DetailView):
    model = Cycle
    template_name = 'cycle_details.html'
    context_object_name = 'cycle'

class ActivityListView(ListView):
    model = Activity
    template_name = 'activities.html'
    context_object_name = 'activities'
    ordering = ['-timestamp']

class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity_details.html'
    context_object_name = 'activity'


class ActivityCreateView(CreateView):
    model = Activity
    fields = ['title', 'time', 'perceived effort', 'notes', 'planned']
    template_name = 'activity_form.html'

    def get_initial(self):
        """get cycle that was passed in or the current cycle if not"""
        initial = super().get_initial()

        cycle_id = self.kwargs.get('cycle_id')

        if cycle_id:
            initial['cycle'] = cycle_id
        else:
            latest_cycle = Cycle.objects.order_by('-id').first()
            if latest_cycle:
                initial['cycle'] = latest_cycle.id
        return initial


    def get_context_data(self, **kwargs):



    def form_valid(self, form):
        pass



