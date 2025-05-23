# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',) # Add email to signup form

class CustomUserChangeForm(UserChangeForm): 
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name') # Fields user can change
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to form fields for better styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'})
