from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(choices=[('', 'Any')] + [(pa, pa) for pa in Voter.objects.values_list('party_affiliation', flat=True).distinct()], required=False)
    min_birth_year = forms.IntegerField(label="Born After (Year)", required=False)
    max_birth_year = forms.IntegerField(label="Born Before (Year)", required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + [(str(i), str(i)) for i in range(6)], required=False)
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)
