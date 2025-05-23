# tasks/forms.py
from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        # Pop the 'user' from kwargs if it's passed, as we'll use it to filter categories
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Apply Tailwind classes to form fields for better styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.Select, forms.DateTimeInput)):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'rounded border-gray-300 text-blue-600 shadow-sm focus:ring-blue-500'})

        # Filter category choices based on the current user's categories
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user)
        else:
            # If no user is provided (e.g., in admin or other contexts), show no categories
            self.fields['category'].queryset = Category.objects.none()

        self.fields['category'].required = False
        self.fields['category'].empty_label = "No Category"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description'] # 'user' field is excluded as it will be set automatically by the view
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Work, Personal, Shopping'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'A brief description of this category'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'})
