from django import forms
from journals.models import Journal

class JournalForm(forms.ModelForm):

    class Meta:
        model = Journal
        fields = ['public', 'title', 'body', 'tags',]
        labels = {
            'public': 'check here to make this post visible to others',
            'title': 'title',
            'body': 'what are you thankful for today?',
            'tags': 'enter tags below separated by a space \n "multi-word tags" get quotation marks'
        }
