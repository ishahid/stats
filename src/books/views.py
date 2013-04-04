from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import string, random

from books.models import Book, Word, WordCount
from books.forms import BookUploadForm

def index(request):
    books = Book.objects.order_by('title')
    return render(request, 'books/index.html', {'books': books})

def book(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, 'books/book.html', {'book': book})

def add(request):
    # Handle file upload
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            process_file(request.FILES['txt_book'])

            # Redirect to the book list after POST
            return HttpResponseRedirect(reverse('books.views.index'))
    else:
        form = BookUploadForm() # An empty, unbound form
        return render(request, 'books/add.html', {'form': form})

def process_file(fp):
    book = read_gutenberg_headers(fp)
    book.save()

    hist = {}
    for line in fp:
        if line.startswith('*** END OF THIS PROJECT GUTENBERG EBOOK'):
            break;
            
        process_line(line, hist)
    
    for key in hist.keys():
        word = Word(text=key)
        word.save()

        count = WordCount(book=book, word=word, count=hist[key])
        count.save()

def read_gutenberg_headers(fp):
    book = Book()
    for line in fp:
        if line.startswith('Title:'):
            book.title = line[6:].strip(string.punctuation + string.whitespace)

        if line.startswith('Author:'):
            book.author = line[7:].strip(string.punctuation + string.whitespace)

        if line.startswith('Release Date:'):
            book.published = line[13:].strip(string.punctuation + string.whitespace)

        if line.startswith('*** START OF THIS PROJECT GUTENBERG EBOOK'):
            return book


def process_line(line, hist):
    # replace hyphens with spaces before splitting
    line = line.replace('-', ' ')
    
    for word in line.split():
        # remove punctuation and convert to lowercase
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()

        # update the histogram
        if len(word) > 0:
            hist[word] = hist.get(word, 0) + 1
