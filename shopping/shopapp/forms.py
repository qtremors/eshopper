from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom User model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'address', 'phone')  # Include all fields
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.address = self.cleaned_data['address']
        user.phone = self.cleaned_data['phone']
        # You'll need to set the password explicitly
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user