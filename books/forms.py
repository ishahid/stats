from django import forms
from django.utils.safestring import mark_safe


class BookUploadForm(forms.Form):
    txt_book = forms.FileField(
                label = 'Upload an ebook in TXT format...',
                help_text = mark_safe('Make sure that it is a '
                                      '<a target="_blank" href="http://www.gutenberg.org">Project Gutenberg</a>'
                                      ' ebook in TXT format.'),
                required = True,
                error_messages = {
                    'required': 'You must give a file to crunch.'
                }
             )
