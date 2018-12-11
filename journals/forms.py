from django import forms
from journals.models import Journal

class JournalForm(forms.ModelForm):

    class Meta:
        model = Journal
        fields = ['public', 'title', 'body', 'tags',]
        labels = {
            'public': 'Public',
            'title': 'Title',
            'body': 'What are you thankful for today?',
            'tags': 'Enter tags below separated by a space.  Use quotation marks for multi-word tags.'
        }
