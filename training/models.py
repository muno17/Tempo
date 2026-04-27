from functools import cached_property
from datetime import timedelta

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    PREFERRED_UNITS_CHOICES = [
        ("mi", "Miles"),
        ("km", "Kilometers"),
    ]
    preferred_units = models.CharField(choices=PREFERRED_UNITS_CHOICES,default='mi', max_length=2)

    default_cycle_name = models.CharField(default='Week', max_length=50)
    default_cycle_length = models.PositiveIntegerField(default=7)
    default_shoe = models.ForeignKey('Shoe', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username}\'s Profile'


class Shoe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    is_retired = models.BooleanField(default=False)
    init_mileage = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.nickname:
            return f'{self.nickname}'
        return f'{self.brand} {self.model_name}'

    # set shoe to always be ordered by newest to oldest
    class Meta:
        ordering = ['-date_added']

    @property
    def mileage(self):
        """Returns the total mileage of the shoe"""
        activity_miles = Segment.objects.filter(
            # Q lets us run an 'or' operation on a query
            models.Q(shoe=self) | models.Q(shoe__isnull=True, activity__default_shoe=self)
        ).aggregate(total=models.Sum('distance'))['total'] or 0

        return float(self.init_mileage) + float(activity_miles)


class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    @cached_property
    def mileage(self):
        """Returns the total mileage of the block"""
        block_miles = self.cycles.aggregate(
            total=models.Sum('activities__segments__distance')
        )['total'] or 0

        return float(block_miles)

    @cached_property
    def time(self):
        """Returns the total time spent running for the block"""
        block_time = self.cycles.aggregate(
            total=models.Sum('activities__segments__duration')
        )['total'] or 0

        if not block_time:
            return timedelta(0)

        return block_time

    @property
    def time_display(self):
        """Returns the total time spent running for the block in a user friendly format"""
        time = self.time
        return str(time).split('.')[0]

    time_display.fget.short_description = 'Total Time'

    @property
    def pace(self):
        """Returns the average pace of the block"""
        miles = float(self.mileage)
        duration = self.time

        if miles <= 0 or not duration:
            return "0:00"

        total_seconds = duration.total_seconds()
        seconds_per_mile = total_seconds / miles

        minutes = int(seconds_per_mile // 60)
        seconds = int(seconds_per_mile % 60)
        return f'{minutes}:{seconds:02d}'

    pace.fget.short_description = "Pace (/mi)"


class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='cycles')
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f'{self.start} {self.end}'

    @cached_property
    def mileage(self):
        """Returns the total mileage of the cycle"""
        cycle_miles = self.activities.aggregate(
            total=models.Sum('segments__distance')
        )['total'] or 0

        return float(cycle_miles)

    @cached_property
    def time(self):
        """Returns the total time spent running for the cycle"""
        cycle_time = self.activities.aggregate(
            total=models.Sum('segments__duration')
        )['total'] or 0

        if not cycle_time:
            return timedelta(0)

        return cycle_time

    @property
    def time_display(self):
        """Returns the total time spent running for the cycle in a user friendly format"""
        time = self.time
        return str(time).split('.')[0]

    time_display.fget.short_description = 'Total Time'

    @property
    def pace(self):
        """Returns the average pace of the cycle"""
        miles = float(self.mileage)
        duration = self.time

        if miles <= 0 or not duration:
            return "0:00"

        total_seconds = duration.total_seconds()
        seconds_per_mile = total_seconds / miles

        minutes = int(seconds_per_mile // 60)
        seconds = int(seconds_per_mile % 60)

        return f'{minutes}:{seconds:02d}'

    pace.fget.short_description = "Pace (/mi)"


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='activities')
    planned = models.BooleanField(default=False)
    title = models.CharField(max_length=100, default='Daily Run')
    timestamp = models.DateTimeField(default=timezone.now)
    perceived_effort = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
    )
    default_shoe = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='activities')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} {self.timestamp}'

    @cached_property
    def mileage(self):
        """Returns the total mileage of the activity"""
        activity_miles = self.segments.aggregate(
            total=models.Sum('distance')
        )['total'] or 0

        return float(activity_miles)

    @cached_property
    def time(self):
        """Returns the total time spent running for the activity"""
        activity_time = self.segments.aggregate(
            total=models.Sum('duration')
        )['total'] or 0

        if not activity_time:
            return timedelta(0)

        return activity_time

    @property
    def time_display(self):
        """Returns the total time spent running for the activity in a user friendly format"""
        time = self.time
        return str(time).split('.')[0]

    time_display.fget.short_description = 'Time'

    @property
    def pace(self):
        """Returns the average pace of the activity"""
        miles = float(self.mileage)
        duration = self.time

        if miles <= 0 or not duration:
            return "0:00"

        total_seconds = duration.total_seconds()
        seconds_per_mile = total_seconds / miles

        minutes = int(seconds_per_mile // 60)
        seconds = int(seconds_per_mile % 60)

        return f'{minutes}:{seconds:02d}'


    pace.fget.short_description = "Pace (/mi)"


class Segment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='segments')
    shoe = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True, blank=True, related_name='segments')
    distance = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    duration = models.DurationField()
    RUN_TYPES = [
        ("EASY", "Easy"),
        ("WARMUP", "Warmup"),
        ("INTERVAL", "Interval"),
        ("STEADY", "Steady"),
        ("TEMPO", "Tempo"),
        ("SUB-THRESHOLD", "Sub-Threshold"),
        ("THRESHOLD", "Threshold"),
        ("RACE", "Race"),
        ("STRIDE", "Stride"),
        ("SPRINT", "Sprint"),
        ("COOLDOWN", "Cooldown"),
        ("REST", "Rest"),
    ]
    type = models.CharField(choices=RUN_TYPES, default='EASY', max_length=20)

    def __str__(self):
        return f'{self.distance} {self.duration} {self.type}'


    @property
    def shoe_used(self):
        """Returns the segment's shoe or the activity's default"""
        # using this to be able to set a default in the ui
        return self.shoe or self.activity.default_shoe

    @property
    def pace(self):
        """Returns the segment's pace"""
        miles = float(self.distance)
        duration = self.duration

        if miles <= 0 or not duration:
            return "0:00"

        total_seconds = duration.total_seconds()
        seconds_per_mile = total_seconds / miles

        minutes = int(seconds_per_mile // 60)
        seconds = int(seconds_per_mile % 60)
        return f'{minutes}:{seconds:02d}'