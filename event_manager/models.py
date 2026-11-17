from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EventDb(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20)
    venue = models.CharField(max_length=100)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    STATUS_CHOICES = (('upcoming','Upcoming'),
                      ('ongoing', 'Ongoing'),
                      ('completed', 'Completed'),
                      ('cancelled', 'Cancelled'),)
    status = models.CharField(choices=STATUS_CHOICES, default='upcoming')
    created_by = models.ForeignKey(User, on_delete= models.CASCADE,
                                    related_name= 'events_created')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.event_name

class EventMemberDb(models.Model):
    event = models.ForeignKey(EventDb, on_delete=models.CASCADE, related_name='event_member')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_membership')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['event', 'user'], name='unique_event_member')]

    def __str__(self):
        return f"{self.user.username} - {self.event.event_name}"