from django.contrib.auth.models import User
from django.forms import inlineformset_factory, DateInput, SplitDateTimeWidget, SplitDateTimeField
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from .models import Block, Cycle, Activity, Segment, Shoe


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Get the latest block, cycle and activity info"""
        context = super().get_context_data(**kwargs)

        context['latest_block'] = Block.objects.order_by('-id').first()
        context['latest_cycle'] = Cycle.objects.order_by('-id').first()
        context['latest_activities'] = Activity.objects.order_by('-id').all()[:5]
        context['total_miles'] = Segment.objects.aggregate(Sum('distance'))['distance__sum']
        context['total_duration'] = Segment.objects.aggregate(Sum('duration'))['duration__sum']
        context['activity_count'] = Activity.objects.count()
        # longest run
        # average overall pace
        return context


class BlockListView(ListView):
    model = Block
    template_name = 'blocks.html'
    context_object_name = 'blocks'
    ordering = ['-start']

class BlockDetailView(DetailView):
    model = Block
    template_name = 'block_details.html'
    context_object_name = 'current_block'

class BlockCreateView(CreateView):
    model = Block
    fields = ['name', 'start', 'end', 'description', 'goals', 'notes']
    template_name = 'block_create.html'
    success_url = reverse_lazy('block-list')

    def form_valid(self, form):
        """Links the Block to the user"""
        super_user = User.objects.first()
        form.instance.user = super_user
        self.object = form.save()
        return redirect(self.success_url)

    def get_form(self):
        """Have the form render the date fields as date-pickers"""
        form = super().get_form()
        form.fields['start'].widget = DateInput(attrs={'type': 'date'})
        form.fields['end'].widget = DateInput(attrs={'type': 'date'})
        return form

class BlockDeleteView(DeleteView):
    model = Block
    template_name = 'block_delete.html'
    context_object_name = 'current_block'
    success_url = reverse_lazy('block-list')


class BlockUpdateView(UpdateView):
    model = Block
    template_name = 'block_update.html'
    fields = ['name', 'start', 'end', 'description', 'goals', 'notes']
    context_object_name = 'current_block'
    success_url = reverse_lazy('block-list')

class CycleListView(ListView):
    model = Cycle
    template_name = 'cycles.html'
    context_object_name = 'cycles'
    ordering = ['-start']

class CycleDetailView(DetailView):
    model = Cycle
    template_name = 'cycle_details.html'
    context_object_name = 'cycle'

class CycleDeleteView(DeleteView):
    model = Cycle
    template_name = 'cycle_delete.html'
    success_url = reverse_lazy('cycle-list')

class CycleCreateView(CreateView):
    model = Cycle
    fields = ['block', 'start', 'end']
    template_name = 'cycle_create.html'
    success_url = reverse_lazy('cycle-list')

    def get_initial(self):
        """get block that was passed in or the current block if not"""
        initial = super().get_initial()

        block_id = self.kwargs.get('block_id')

        if block_id:
            initial['block'] = block_id
        else:
            latest_block = Block.objects.order_by('-id').first()
            if latest_block:
                initial['block'] = latest_block.id
        return initial

    def get_form(self):
        """Have the form render the date fields as date-pickers"""
        form = super().get_form()
        form.fields['start'].widget = DateInput(attrs={'type': 'date'})
        form.fields['end'].widget = DateInput(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        """Links the Cycle to the segments and saves the activity and segments"""
        super_user = User.objects.first()
        form.instance.user = super_user
        self.object = form.save()
        return redirect(self.success_url)


class CycleUpdateView(UpdateView):
    model = Cycle
    template_name = 'cycle_update.html'
    fields = ['block', 'start', 'end']
    success_url = reverse_lazy('cycle-list')

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
    fields=('distance', 'duration', 'type', 'shoe'),
    extra=7,  # How many empty rows to show by default
    can_delete=True
)
class ActivityCreateView(CreateView):
    model = Activity
    fields = ['title', 'timestamp', 'cycle', 'planned', 'perceived_effort', 'notes']
    template_name = 'activity_create.html'
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

    def get_form(self):
        """Have the form render the timestamp as a date-picker and time field"""
        form = super().get_form()
        # SplitDateTimeWidget separates the datetime so we can have two separate fields
        # SplitDateTimeField joins the date and time fields into a single datetime object
        form.fields['timestamp'] = SplitDateTimeField(
            widget=SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time'}
            )
        )
        return form

    def get_context_data(self, **kwargs):
        """Adds the form's segment info to the context"""
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['segments'] = SegmentFormSet(self.request.POST)
        else:
            context['segments'] = SegmentFormSet()

        return context

    def form_valid(self, form):
        """Links the Activity to the segments and saves the activity and segments"""
        super_user = User.objects.first()

        form.instance.user = super_user
        self.object = form.save()

        context = self.get_context_data()
        segments = context['segments']

        if segments.is_valid():
            # create the segments objects but don't save since we still need to update each one
            seg_instances = segments.save(commit=False)

            # link segment to the superuser and to the activity
            for instance in seg_instances:
                instance.user = super_user
                instance.activity = self.object
                instance.save()

            return redirect(self.success_url)
        else:
            # render form with error messages
            return self.render_to_response(self.get_context_data(form=form))

class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activity_delete.html'
    success_url = reverse_lazy('activity-list')


class ActivityUpdateView(UpdateView):
    model = Activity
    template_name = 'activity_update.html'
    fields = ['title', 'timestamp', 'cycle', 'planned', 'perceived_effort', 'notes']
    success_url = reverse_lazy('activity-list')

    def get_context_data(self, **kwargs):
        """Adds the Activity's segment info to the context"""
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['segments'] = SegmentFormSet(self.request.POST, instance=self.object)
        else:
            context['segments'] = SegmentFormSet(instance=self.object)

        return context

    def get_form(self):
        """Have the form render the timestamp as a date-picker and time field"""
        form = super().get_form()
        # SplitDateTimeWidget separates the datetime so we can have two separate fields
        # SplitDateTimeField joins the date and time fields into a single datetime object
        form.fields['timestamp'] = SplitDateTimeField(
            widget=SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time'}
            )
        )
        return form

    def form_valid(self, form):
        """Links the Activity to the segments, handles updating/deleting segments"""
        super_user = User.objects.first()
        form.instance.user = super_user

        context = self.get_context_data()
        segments = context['segments']
        self.object = form.save()

        if segments.is_valid():
            # create/delete the segments objects but don't save since we still need to update each one
            seg_instances = segments.save(commit=False)

            for seg in segments.deleted_objects:
                seg.delete()

            # link segment to the superuser and to the activity
            for instance in seg_instances:
                instance.user = super_user
                instance.activity = self.object
                instance.save()

            return super().form_valid(form)
        else:
            # render form with error messages
            return self.render_to_response(self.get_context_data(form=form))

class ShoeListView(ListView):
    model = Shoe
    template_name = 'shoes.html'
    context_object_name = 'shoes'
    ordering = ['-date_added']


class ShoeCreateView(CreateView):
    model = Shoe
    template_name = 'shoe_create.html'
    context_object_name = 'shoe'
    fields = ['brand', 'model_name', 'nickname', 'init_mileage', 'is_retired', 'notes']
    success_url = reverse_lazy('shoe-list')


class ShoeDetailView(DetailView):
    model = Shoe
    template_name ='shoe_details.html'
    context_object_name = 'shoe'


class ShoeUpdateView(UpdateView):
    model = Shoe
    template_name = 'shoe_update.html'
    fields = ['brand', 'model_name', 'nickname', 'is_retired', 'notes']
    success_url = reverse_lazy('shoe-list')


class ShoeDeleteView(DeleteView):
    model = Shoe
    template_name = 'shoe_delete.html'
    context_object_name = 'shoe'
    success_url = reverse_lazy('shoe-list')