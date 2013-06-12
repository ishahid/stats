from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from books.forms import BookUploadForm
from books.models import Book, Word
from utils import process_book


def index(request):
    form = BookUploadForm()
    books = Book.objects.order_by('title')
    return render(request, 'books/index.html', {'books': books, 'form': form})


def book(request, id):
    form = BookUploadForm()
    book = get_object_or_404(Book, pk=id)
    return render(request, 'books/book.html', {'book': book, 'form': form})


def add(request):
    # Handle file upload
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                process_book(request.FILES['txt_book'])
            except IntegrityError as error:
                return render(request, 'books/error.html', {'error': error})

            # Redirect to the book list after POST
            return HttpResponseRedirect(reverse('books.views.index'))
    else:
        form = BookUploadForm()  # An empty, unbound form
        return render(request, 'books/add.html', {'form': form})


def word(request, id):
    form = BookUploadForm()
    word = get_object_or_404(Word, pk=id)
    return render(request, 'books/word.html', {'word': word, 'form': form})
