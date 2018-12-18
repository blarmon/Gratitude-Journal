from django import forms
from journals.models import Journal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class JournalForm(forms.ModelForm):

    class Meta:
        model = Journal
        fields = ['public', 'title', 'body', 'tags', ]
        labels = {
            'public': 'check here to make this post visible to others',
            'title': 'title',
            'body': 'what are you thankful for today?',
            'tags': 'enter tags below separated by a space \n "multi-word tags" get quotation marks'
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Please enter a valid email \n', label='\nEmail:', label_suffix='')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )