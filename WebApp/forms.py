from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="First name")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        # first_name, last_name = self.cleaned_data["fullname"].split()
        # user.first_name = first_name
        # user.last_name = last_name
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
