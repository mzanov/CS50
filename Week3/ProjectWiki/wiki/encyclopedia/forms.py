from django import forms


class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'cols': 20, 'rows': 4}))

class EntryForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'cols': 20, 'rows': 4}))
