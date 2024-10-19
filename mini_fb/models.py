from django.db import models
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f'{self.profile.first_name} - {self.message[:20]}'
    
    def get_images(self):
        """Return all images associated with this status message."""
        return self.images.all()
    
class Image(models.Model):
    image_file = models.ImageField(upload_to='status_images/')
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.status_message.message[:20]} uploaded on {self.timestamp}"