from django import forms
from .models import UserProfile, Review, Movie

# CreateProfileForm is used to create a new user profile with necessary fields like first name, last name, email, etc.
class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # The model this form is based on
        fields = ['first_name', 'last_name', 'email', 'profile_image_url', 'birthdate']  # Fields that will be used in the form

# UpdateProfileForm is used to update an existing user's profile (e.g., email, profile picture, and birthdate)
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # The model this form is based on
        fields = ['email', 'profile_image_url', 'birthdate']  # Fields to update in the user's profile

# CreateReviewForm is used to create a new review for a movie
class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # The model this form is based on
        fields = ['movie', 'rating', 'review_text']  # Fields included in the review form
        widgets = {
            'movie': forms.Select(),  # Dropdown menu for selecting a movie
            'rating': forms.RadioSelect(),  # Radio buttons for selecting a rating
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'})  # Textarea for review text
        }

    def clean_movie(self):
        # Ensure that a movie is selected (i.e., the movie field is required)
        movie = self.cleaned_data.get('movie')
        if not movie:
            raise forms.ValidationError("This field is required.")
        return movie

# CreateMovieForm is used to create a new movie entry, with fields like title, description, and more
class CreateMovieForm(forms.ModelForm):
    class Meta:
        model = Movie  # The model this form is based on
        fields = ['title', 'description', 'release_date', 'director', 'genre', 'poster']  # Fields to include in the movie creation form
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),  # Date input widget for release date
        }

# UpdateReviewForm is used to update an existing review, such as rating or review text
class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # The model this form is based on
        fields = ['rating', 'review_text']  # Fields to update in an existing review
