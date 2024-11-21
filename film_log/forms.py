from django import forms
from .models import Profile, Review

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_image_url', 'birthdate']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
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
