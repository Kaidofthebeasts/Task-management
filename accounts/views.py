# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView 
from django.contrib.auth.mixins import LoginRequiredMixin 

from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser 


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class ProfileView(LoginRequiredMixin, UpdateView): 
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile.html' 
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Ensure the user can only edit their own profile
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a placeholder for password change URL
        context['password_change_url'] = reverse_lazy('password_change')
        return context
