from django.contrib.auth.models import User
from django.forms import inlineformset_factory, NumberInput, TextInput, DateInput, SplitDateTimeWidget, SplitDateTimeField, TimeInput
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum, Max
from .models import Block, Cycle, Activity, Segment, Shoe

def get_target_user(request):
    if request.user.is_authenticated:
        return request.user
    # get demo user for guests
    return User.objects.get(username='demo')
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Get the latest block, cycle and activity info"""
        context = super().get_context_data(**kwargs)

        context['latest_block'] = Block.objects.filter(user=get_target_user(self.request)).order_by('-id').first()
        context['latest_cycle'] = Cycle.objects.filter(user=get_target_user(self.request)).order_by('-id').first()
        context['latest_activities'] = Activity.objects.filter(user=get_target_user(self.request)).order_by('-id').all()[:5]
        context['total_duration'] = Segment.objects.filter(user=get_target_user(self.request)).aggregate(Sum('duration'))['duration__sum']
        context['activity_count'] = Activity.objects.filter(user=get_target_user(self.request)).count()
        context['longest_duration'] = Activity.objects.filter(user=get_target_user(self.request)).annotate(
            total_duration=Sum('segments__duration')
        ).aggregate(Max('total_duration'))['total_duration__max'] or 0.0

        longest_run = Activity.objects.filter(user=get_target_user(self.request)).annotate(
            total_miles=Sum('segments__distance')
        ).aggregate(Max('total_miles'))['total_miles__max'] or 0.0
        if longest_run:
            context['longest_run'] = round(longest_run, 2)

        total_miles = Segment.objects.filter(user=get_target_user(self.request)).aggregate(Sum('distance'))['distance__sum']
        if total_miles:
            context['total_miles'] = round(total_miles, 2)

        return context


class BlockListView(ListView):
    model = Block
    template_name = 'blocks.html'
    context_object_name = 'blocks'
    ordering = ['-start']

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

class BlockDetailView(DetailView):
    model = Block
    template_name = 'block_details.html'
    context_object_name = 'current_block'

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

class BlockCreateView(CreateView):
    model = Block
    fields = ['name', 'start', 'end', 'description', 'goals', 'notes']
    template_name = 'block_create.html'
    success_url = reverse_lazy('block-list')

    def form_valid(self, form):
        """Links the Block to the user"""
        form.instance.user = get_target_user(self.request)
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

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)


class BlockUpdateView(UpdateView):
    model = Block
    template_name = 'block_update.html'
    fields = ['name', 'start', 'end', 'description', 'goals', 'notes']
    context_object_name = 'current_block'
    success_url = reverse_lazy('block-list')

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

class CycleListView(ListView):
    model = Cycle
    template_name = 'cycles.html'
    context_object_name = 'cycles'
    ordering = ['-start']

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

class CycleDetailView(DetailView):
    model = Cycle
    template_name = 'cycle_details.html'
    context_object_name = 'cycle'

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

class CycleDeleteView(DeleteView):
    model = Cycle
    template_name = 'cycle_delete.html'
    success_url = reverse_lazy('cycle-list')

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

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
            latest_block = Block.objects.filter(user=get_target_user(self.request)).order_by('-id').first()
            if latest_block:
                initial['block'] = latest_block.id
        return initial

    def get_form(self):
        """Have the form render the date fields as date-pickers"""
        form = super().get_form()
        form.fields['start'].widget = DateInput(attrs={'type': 'date'})
        form.fields['end'].widget = DateInput(attrs={'type': 'date'})

        user = get_target_user(self.request)
        if 'cycle' in form.fields:
            form.fields['cycle'].queryset = Cycle.objects.filter(user=user)
        if 'block' in form.fields:
            form.fields['block'].queryset = Block.objects.filter(user=user)

        return form

    def form_valid(self, form):
        """Links the Cycle to the segments and saves the activity and segments"""
        form.instance.user = get_target_user(self.request)
        self.object = form.save()
        return redirect(self.success_url)


class CycleUpdateView(UpdateView):
    model = Cycle
    template_name = 'cycle_update.html'
    fields = ['block', 'start', 'end']
    success_url = reverse_lazy('cycle-list')

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

class ActivityListView(ListView):
    model = Activity
    template_name = 'activities.html'
    context_object_name = 'activities'
    ordering = ['-timestamp']

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity_details.html'
    context_object_name = 'activity'

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)


# formset is needed to have a nested form for segments within an activity
SegmentFormSet = inlineformset_factory(
    Activity, Segment,
    fields=('distance', 'duration', 'type', 'shoe'),
    extra=7,  # How many empty rows to show by default
    can_delete=True,
    widgets={
        'duration': TextInput(attrs={
            'placeholder': 'hh:mm:ss',
            'class': 'form-control', # or whatever CSS class you use
            'style': 'width: 100px;'
        }),
        'distance': NumberInput(attrs={
            'step': '0.00001',  # Tells the browser and Django to allow high precision
            'class': 'form-control',
        }),
    },
)


class ActivityUtilityMixin():
    def get_context_data(self, **kwargs):
        """Adds the Activity's segment info to the context"""
        context = super().get_context_data(**kwargs)
        user = get_target_user(self.request)

        if self.request.POST:
            formset = SegmentFormSet(self.request.POST, instance=self.object)
        else:
            formset = SegmentFormSet(instance=self.object)

        # get the right shoes for the user to display
        for form in formset.forms:
            form.fields['shoe'].queryset = Shoe.objects.filter(user=user)

        context['segments'] = formset
        return context

    def get_form(self):
        """Have the form render the timestamp as a date-picker and time field"""
        form = super().get_form()
        user = get_target_user(self.request)
        if 'cycle' in form.fields:
            form.fields['cycle'].queryset = Cycle.objects.filter(user=user)
        if 'block' in form.fields:
            form.fields['block'].queryset = Block.objects.filter(user=user)
        if 'default_shoe' in form.fields:
            form.fields['default_shoe'].queryset = Shoe.objects.filter(user=user)
        # SplitDateTimeWidget separates the datetime so we can have two separate fields
        # SplitDateTimeField joins the date and time fields into a single datetime object
        form.fields['timestamp'] = SplitDateTimeField(
            widget=SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time'}
            )
        )
        return form


class ActivityCreateView(ActivityUtilityMixin, CreateView):
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

    def form_valid(self, form):
        """Links the Activity to the segments and saves the activity and segments"""
        form.instance.user = get_target_user(self.request)
        self.object = form.save()

        context = self.get_context_data()
        segments = context['segments']

        if segments.is_valid():
            # check the unit preference
            unit_type = self.request.POST.get('unit_type', 'mi')

            # create the segments objects but don't save since we still need to update each one
            seg_instances = segments.save(commit=False)

            # link segment to the superuser and to the activity
            for instance in seg_instances:
                instance.user = get_target_user(self.request)
                instance.activity = self.object

                # conver distance if the user input in km
                if unit_type == 'km':
                    instance.distance = float(instance.distance) / 1.60934

                instance.save()

            return redirect(self.success_url)
        else:
            # render form with error messages
            return self.render_to_response(self.get_context_data(form=form))

class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activity_delete.html'
    success_url = reverse_lazy('activity-list')

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)


class ActivityUpdateView(ActivityUtilityMixin, UpdateView):
    model = Activity
    template_name = 'activity_update.html'
    fields = ['title', 'timestamp', 'cycle', 'planned', 'perceived_effort', 'notes']
    success_url = reverse_lazy('activity-list')

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)

    def form_valid(self, form):
        """Links the Activity to the segments, handles updating/deleting segments"""
        form.instance.user = get_target_user(self.request)

        context = self.get_context_data()
        segments = context['segments']
        self.object = form.save()

        if segments.is_valid():
            # check the unit preference
            unit_type = self.request.POST.get('unit_type', 'mi')

            # create/delete the segments objects but don't save since we still need to update each one
            seg_instances = segments.save(commit=False)

            for seg in segments.deleted_objects:
                seg.delete()

            # link segment to the superuser and to the activity
            for instance in seg_instances:
                instance.user = get_target_user(self.request)
                instance.activity = self.object

                # conver distance if the user input in km
                if unit_type == 'km':
                    instance.distance = float(instance.distance) / 1.60934

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

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)


class ShoeCreateView(CreateView):
    model = Shoe
    template_name = 'shoe_create.html'
    context_object_name = 'shoe'
    fields = ['brand', 'model_name', 'nickname', 'init_mileage', 'init_duration', 'is_retired', 'notes']
    success_url = reverse_lazy('shoe-list')

    def form_valid(self, form):
        form.instance.user = get_target_user(self.request)
        return super().form_valid(form)


class ShoeDetailView(DetailView):
    model = Shoe
    template_name ='shoe_details.html'
    context_object_name = 'shoe'

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)


class ShoeUpdateView(UpdateView):
    model = Shoe
    template_name = 'shoe_update.html'
    fields = ['brand', 'model_name', 'nickname', 'is_retired', 'notes']
    success_url = reverse_lazy('shoe-list')

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)


class ShoeDeleteView(DeleteView):
    model = Shoe
    template_name = 'shoe_delete.html'
    context_object_name = 'shoe'
    success_url = reverse_lazy('shoe-list')

    def get_queryset(self):
        user = get_target_user(self.request)
        return super().get_queryset().filter(user=user)