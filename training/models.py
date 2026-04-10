from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PREFERRED_UNITS_CHOICES = [
        ("mi", "Miles"),
        ("km", "Kilometers"),
    ]
    preferred_units = models.CharField(choices=PREFERRED_UNITS_CHOICES,default='mi', max_length=2)

    cycle_length = models.CharField(default='week', max_length=50)
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

    # property for total mileage

    def __str__(self):
        return f'{self.brand} {self.model_name} {self.nickname}'

class Block(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    goals = models.TextField(null=True, blank=True)

    # property for total duration
    # property for total distance

    def __str__(self):
        return f'{self.name}'

class Cycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='cycles')
    start = models.DateField()
    end = models.DateField()

    # property for total duration
    # property for total distance

    def __str__(self):
        return f'{self.start} {self.end}'

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='activities')
    planned = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    total_time = models.DurationField()
    timestamp = models.DateTimeField()
    perceived_effort = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
    )
    shoe = models.ForeignKey(Shoe, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='activities')
    notes = models.TextField(null=True, blank=True)

    # property for total duration
    # property for total distance

    def __str__(self):
        return f'{self.title} {self.total_time} {self.timestamp}'


class Segment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='segments')
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
