from django import forms

class BookUploadForm(forms.Form):
    txt_book = forms.FileField(
                label = 'Select a file',
                help_text = 'Make sure that it is a Project Gutenberg TXT book.'
             )
