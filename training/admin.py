from django.contrib import admin
from .models import Profile, Shoe, Block, Cycle, Activity, Segment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "preferred_units", "default_cycle_length",
                    "default_cycle_name", "default_shoe")


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ("brand", "model_name", "nickname", "shoe_mileage", "user",
                    "date_added", "is_retired")
    list_filter = ("user", "brand", "model_name")

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "block_mileage", "block_time_display", "start", "end")
    list_filter = ("user", "name")


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ("start", "end", "cycle_mileage", "cycle_time_display", "user")
    list_filter = ("user", "start", "end")


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "timestamp", "activity_mileage",
                    "activity_time_display", "perceived_effort")
    list_filter = ("user", "timestamp")


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ("distance", "duration", "type", "user")
    list_filter = ("user", "type")