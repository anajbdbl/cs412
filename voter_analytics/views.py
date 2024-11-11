from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Voter
import plotly.express as px
import plotly.graph_objects as go
from django.db.models import Count
from .forms import VoterFilterForm


# Create your views here.
class VoterListView(ListView):
    model = Voter
    paginate_by = 100 
    template_name = 'voter_analytics/voter_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Instantiate the filter form with GET parameters
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            # Apply each filter if it has been set in the GET parameters
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_birth_year'])
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_birth_year'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['v20state']:
                queryset = queryset.filter(v20state=True)
            if form.cleaned_data['v21town']:
                queryset = queryset.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                queryset = queryset.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                queryset = queryset.filter(v22general=True)
            if form.cleaned_data['v23town']:
                queryset = queryset.filter(v23town=True)
        return queryset

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'

class GraphsView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Instantiate the filter form with GET parameters
        form = VoterFilterForm(self.request.GET)
        voters = Voter.objects.all()
        
        # Apply form filters if valid
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                voters = voters.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth_year']:
                voters = voters.filter(date_of_birth__year__gte=form.cleaned_data['min_birth_year'])
            if form.cleaned_data['max_birth_year']:
                voters = voters.filter(date_of_birth__year__lte=form.cleaned_data['max_birth_year'])
            if form.cleaned_data['voter_score']:
                voters = voters.filter(voter_score=form.cleaned_data['voter_score'])
            if form.cleaned_data['v20state']:
                voters = voters.filter(v20state=True)
            if form.cleaned_data['v21town']:
                voters = voters.filter(v21town=True)
            if form.cleaned_data['v21primary']:
                voters = voters.filter(v21primary=True)
            if form.cleaned_data['v22general']:
                voters = voters.filter(v22general=True)
            if form.cleaned_data['v23town']:
                voters = voters.filter(v23town=True)

        # Create the graphs with the filtered data
        # Histogram of voter birth years
        birth_years = [v.date_of_birth.year for v in voters if v.date_of_birth]
        birth_year_fig = px.histogram(birth_years, title="Distribution by Year of Birth")

        # Pie chart for party affiliation
        party_counts = voters.values('party_affiliation').annotate(count=Count('party_affiliation'))
        party_fig = px.pie(party_counts, values='count', names='party_affiliation', title="Party Affiliation Distribution")

        # Bar chart for participation in elections
        election_participation = {
            '2020 State': voters.filter(v20state=True).count(),
            '2021 Town': voters.filter(v21town=True).count(),
            '2021 Primary': voters.filter(v21primary=True).count(),
            '2022 General': voters.filter(v22general=True).count(),
            '2023 Town': voters.filter(v23town=True).count(),
        }
        election_fig = px.bar(x=election_participation.keys(), y=election_participation.values(), title="Participation in Recent Elections")

        # Add form and graphs to the context
        context['filter_form'] = form
        context['birth_year_fig'] = birth_year_fig.to_html()
        context['party_fig'] = party_fig.to_html()
        context['election_fig'] = election_fig.to_html()

        return context