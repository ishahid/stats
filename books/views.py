from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from books.forms import BookUploadForm
from books.models import Book
from utils import process_book, get_word_cloud


def index(request):
    books = Book.objects.order_by('title')
    return render(request, 'books/index.html', {'books': books})


def book(request, id):
    book = get_object_or_404(Book, pk=id)
    percentage_u = float(book.get_unique_words()) / book.get_total_words() * 100
    percentage_t = 100 - percentage_u
    cloud = get_word_cloud(book.get_most_common_words(100))
    return render(request, 'books/book.html', {'book': book, 'cloud': cloud, 'percentage_u': percentage_u, 'percentage_t': percentage_t})


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


