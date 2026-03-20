from django.contrib import admin
from .models import PetReport, Notification

@admin.register(PetReport)
class PetReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'report_type', 'pet_type', 'status', 'user', 'created_at']
    list_filter = ['status', 'report_type', 'pet_type']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notif_type', 'is_read', 'created_at']