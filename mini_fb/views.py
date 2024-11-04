from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile_pk = self.kwargs.get("pk")
        return get_object_or_404(Profile, pk=profile_pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()

        if self.request.user.is_authenticated:
            try:
                context['user_profile_pk'] = self.request.user.profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None

        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        #profile_form = self.get_form(self.get_form_class())

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)

            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            self.object = profile

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile

        sm = form.save()

        files = self.request.FILES.getlist('files')
        for file in files:
            Image.objects.create(image_file=file, status_message=sm)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm  
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        # Ensure that only the owner of the profile can update it
        return get_object_or_404(Profile, user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None
        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'

    def form_valid(self, form):
        sm = form.save()

        # Handle new uploaded files 
        files = self.request.FILES.getlist('files')
        for file in files:
            Image.objects.create(image_file=file, status_message=sm)
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None
        return context
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None
        return context
    
class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'mini_fb/delete_image_form.html'

    def get_success_url(self):
        return reverse_lazy('update_status', kwargs={'pk': self.object.status_message.pk})
    
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=self.request.user)
        other = get_object_or_404(Profile, pk=kwargs['other_pk'])

        profile.add_friend(other)

        return redirect('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()

        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None

        return context
    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()

        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_profile_pk'] = user_profile.pk
            except Profile.DoesNotExist:
                context['user_profile_pk'] = None

        return context