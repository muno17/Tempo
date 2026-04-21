from datetime import datetime

from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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


# formset is needed to have a nested form for segments within an activity
SegmentFormSet = inlineformset_factory(
    Activity, Segment,
    fields=('distance', 'duration', 'type'),
    extra=3,  # How many empty rows to show by default
    can_delete=True
)
class ActivityCreateView(CreateView):
    model = Activity
    fields = ['title', 'timestamp', 'perceived_effort', 'notes', 'planned']
    template_name = 'activity_form.html'
    success_url = reverse_lazy('activity-list')

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
        """Adds the form's segment info to the context"""
        context = super().get_context_data(**kwargs)

        #context['current_time'] = datetime.now()
        if self.request.POST:
            context['segments'] = SegmentFormSet(self.request.POST)
        else:
            context['segments'] = SegmentFormSet()

        return context

    def form_valid(self, form):
        """Links the Activity to the segments and saves the activity and segments"""
        self.object = form.save()

        context = self.get_context_data()
        segments = context['segments']

        if segments.is_valid():
            segments.instance = self.object
            segments.save()
            return redirect(self.success_url)
        else:
            # render form with error messages
            return self.render_to_response(self.get_context_data(form=form))





