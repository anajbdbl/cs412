from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage, Image

# Create your views here.

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        form.instance.profile = profile

        sm = form.save()

        files = self.request.FILES.getlist('files')
        for file in files:
            Image.objects.create(image_file=file, status_message=sm)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm  
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class UpdateStatusMessageView(UpdateView):
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
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class DeleteImageView(DeleteView):
    model = Image
    template_name = 'mini_fb/delete_image_form.html'

    def get_success_url(self):
        """Redirect to the status message update page after deletion."""
        return reverse_lazy('update_status', kwargs={'pk': self.object.status_message.pk})