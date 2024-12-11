from django import forms
from .models import UserProfile, Review, Movie

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'profile_image_url', 'birthdate']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'profile_image_url', 'birthdate']

class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'rating', 'review_text']
        widgets = {
            'movie': forms.Select(),
            'rating': forms.RadioSelect(),
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'})
        }

    def clean_movie(self):
        movie = self.cleaned_data.get('movie')
        if not movie:
            raise forms.ValidationError("This field is required.")
        return movie

class CreateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'director', 'genre', 'poster']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),  # Date input widget for release date
        }

class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']