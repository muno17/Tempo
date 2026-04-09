from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ForeignKey, CharField


class Profile(models.Model):
    PREFERRED_UNITS_CHOICES = {
        "mi": "Miles",
        "km": "Kilometers"
    }
    preferred_units = models.CharField(
        choices=PREFERRED_UNITS_CHOICES,
        default='mi',
    )

    cycle_length = models.CharField(default='week')
    default_shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)

    def __str__(self):
        return 'profile'

class Shoe(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    is_retired = models.BooleanField(default=False)
    init_mileage = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

class Block(models.Model):
    start = models.DateField()
    end = models.DateField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return 'block'

class Cycle(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return 'cycle'

class Activity(models.Model):
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    planned = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    total_time = models.DurationField()
    timestamp = models.DateTimeField()
    perceived_effort = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
    )
    shoe = models.CharField


class Segment(models.Model):
    pass
