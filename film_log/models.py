from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    profile_image_url = models.URLField(max_length=200)
    birthdate = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_reviews(self):
        return self.reviews.all().order_by('-timestamp')

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

    def get_home(self):
        own_messages = Review.objects.filter(profile=self)
        friend_profiles = self.get_friends()
        friend_messages = Review.objects.filter(profile__in=friend_profiles)
        all_messages = own_messages | friend_messages
        
        return all_messages.order_by('-timestamp')

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    director = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    review_text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s Watchlist: {self.movie.title}"
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_set1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_set2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"