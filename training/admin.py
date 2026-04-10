from django.contrib import admin
from .models import Profile, Shoe, Block, Cycle, Activity, Segment

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "preferred_units", "cycle_length", "default_shoe")


@admin.register(Shoe)
class ShoeAdmin(admin.ModelAdmin):
    list_display = ("brand", "model_name", "nickname", "user", "date_added", "is_retired")
    list_filter = ("user", "brand", "model_name")

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "start", "end")
    list_filter = ("user", "name")


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ("start", "end", "user")
    list_filter = ("user", "start", "end")


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "timestamp", "total_time", "perceived_effort")
    list_filter = ("user", "timestamp", "total_time")

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ("distance", "duration", "type", "user")
    list_filter = ("user", "type")