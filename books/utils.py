import string, math
from django.core.exceptions import ObjectDoesNotExist
from books.models import Book, Word, WordCount
from django.utils.safestring import mark_safe


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


def get_word_cloud(list):
    hist = {}
    for wc in list:
        hist[wc.word.text] = wc.count

    f_max = 64
    t_min = hist[min(hist, key=hist.get)]
    t_max = hist[max(hist, key=hist.get)]

    cloud = ''
    for word in sorted(hist.keys()):
        freq = hist[word]
        t_i = freq
        if t_i > t_min:
            s_i = (f_max*(t_i-t_min))/(t_max-t_min)
            s_i = int(math.fabs(s_i))
            if s_i == 0:
                s_i = 1
            else:
                s_i = math.log10(s_i)
        else:
            s_i = 1

        s_i = int(s_i * 30)

        cloud = cloud + '<span style="font-size:' + str(s_i) + 'px;">' + word + '</span> '

    return mark_safe(cloud)
