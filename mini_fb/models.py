from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)
    birthdate = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile') # assignment 9 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')

    def get_friends(self):
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        
        return [friend.profile2 if friend.profile1 == self else friend.profile1 for friend in friends]
    
    def add_friend(self, other):
        if not Friend.objects.filter(models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)).exists():
            Friend.objects.create(profile1=self, profile2=other, timestamp=timezone.now())

    def get_friend_suggestions(self):
        current_friends = set(self.get_friends())
        all_profiles = set(Profile.objects.exclude(pk=self.pk))
        return list(all_profiles - current_friends)

    def get_news_feed(self):
        own_messages = StatusMessage.objects.filter(profile=self)
        friend_profiles = self.get_friends()
        friend_messages = StatusMessage.objects.filter(profile__in=friend_profiles)
        all_messages = own_messages | friend_messages
        
        return all_messages.order_by('-timestamp')

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
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_set1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_set2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Display the friendship as a string."""
        return f"{self.profile1} & {self.profile2}"