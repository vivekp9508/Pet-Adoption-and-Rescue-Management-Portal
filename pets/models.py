from django.db import models
from django.conf import settings

class PetReport(models.Model):
    REPORT_TYPE = [('lost', 'Lost'), ('found', 'Found')]
    STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]
    PET_TYPES = [('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('other', 'Other')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES)
    breed = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contact_info = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.report_type.upper()} - {self.pet_type} ({self.status})"


class Notification(models.Model):
    NOTIF_TYPES = [
        ('report_submitted', 'Report Submitted'),
        ('status_updated', 'Status Updated'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notif_type = models.CharField(max_length=30, choices=NOTIF_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    report = models.ForeignKey(PetReport, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.notif_type}"