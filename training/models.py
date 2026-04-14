from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    is_retired = models.BooleanField(default=False)
    init_mileage = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.brand} {self.model_name} {self.nickname}'

    @property
    def shoe_mileage(self):
        """Returns the total mileage of the shoe"""
        activity_miles = Segment.objects.filter(
            # Q lets us run an 'or' operation on a query
            models.Q(shoe=self) | models.Q(shoe__isnull=True, activity__default_shoe=self)
        ).aggregate(total=models.Sum('distance'))['total'] or 0

        return float(self.init_mileage) + float(activity_miles)

class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)

    # property for total duration

    def __str__(self):
        return f'{self.name}'

    @property
    def block_mileage(self):
        """Returns the total mileage of the block"""
        block_miles = self.cycles.aggregate(
            total=models.Sum('activities__segments__distance')
        )['total'] or 0

        return float(block_miles)


class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='cycles')
    start = models.DateField()
    end = models.DateField()

    # property for total duration

    def __str__(self):
        return f'{self.start} {self.end}'

    def cycle_mileage(self):
        """Returns the total mileage of the cycle"""
        cycle_miles = self.activities.aggregate(
            total=models.Sum('segments__distance')
        )['total'] or 0

        return float(cycle_miles)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    # property for total duration
    @property
    def activity_mileage(self):
        """Returns the total mileage of the activity"""
        activity_miles = self.segments.aggregate(
            total=models.Sum('distance')
        )['total'] or 0

        return float(activity_miles)


class Segment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='segments')
    shoe = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True, blank=True,)
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
    def effective_shoe(self):
        """Returns the segment's shoe or the activity's default"""
        return self.shoe or self.activity.default_shoe