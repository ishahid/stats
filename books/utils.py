import string
from django.core.exceptions import ObjectDoesNotExist
from books.models import Book, Word, WordCount


def process_book(fp):
    book = read_gutenberg_headers(fp)
    book.save()

    hist = {}
    for line in fp:
        if line.startswith('*** END OF THIS PROJECT GUTENBERG EBOOK'):
            break;
            
        process_line(line, hist)
    
    for key in hist.keys():
        try:
            word = Word.objects.get(text=key)
        except ObjectDoesNotExist:
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
