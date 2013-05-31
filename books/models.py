from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe
import math


class Word(models.Model):
    text = models.CharField('Text', max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'word'
        verbose_name_plural = 'words'

    def __unicode__(self):
        return self.text


class Book(models.Model):
    title = models.CharField('Title', max_length=255, unique=True)
    author = models.CharField('Author', max_length=255)
    published = models.CharField('Published', max_length=255, null=True, blank=True)
    
    def get_unique_words(self):
        """Returns count of unique words in this book."""
        return WordCount.objects.filter(book=self).count()

    def get_total_words(self):
        """Returns count of total words in this book."""
        aggregate = WordCount.objects.filter(book=self).aggregate(Sum('count'))
        return aggregate['count__sum']

    def get_most_common_words(self, n=50):
        """Returns N most common words in this book."""
        exclude_list = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on',
                        'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we',
                        'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'did'
                        'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make',
                        'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
                        'good', 'some', 'could', 'them','see', 'other', 'than', 'then', 'now', 'look', 'only', 'come',
                        'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
                        'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'
                        'was', 'were']

        list = WordCount.objects.filter(book=self).exclude(word__text__in=exclude_list).order_by('-count')[:n]
        return list

    def get_word_histogram(self):
        """Returns histogram of the words from this book."""
        words = WordCount.objects.filter(book=self)

        n = words.count()
        k = int(math.floor(math.sqrt(n)));
        h = int(math.floor(n/k));
        hist = {}
        for i in range(0, k, 1):
            hist[h*i] = 0

        bins = hist.keys()
        bins.sort()

        for w in words:
            for bin in bins:
                if w.count < bin:
                    hist[bin] = hist[bin] + 1
                    break

        c_hist = {}
        for key in hist.keys():
            if hist[key] != 0:
                c_hist[key] = hist[key]

        return sorted(c_hist.iteritems())

    def get_word_cloud(self):
        """Returns word cloud from this book based upon the algorithm defined at wikipedia."""
        """http://en.wikipedia.org/wiki/Tag_cloud"""

        hist = {}
        list = self.get_most_common_words(100)
        for wc in list:
            hist[wc.word.text] = wc.count

        f_max = 60
        t_min = hist[min(hist, key=hist.get)]
        t_max = hist[max(hist, key=hist.get)]

        cloud = {}
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

            s_i = int(s_i * 25)

            cloud[word] = [freq, s_i]

        return sorted(cloud.iteritems())

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __unicode__(self):
        return self.title


class WordCount(models.Model):
    book = models.ForeignKey(Book, related_name='fk_book')
    word = models.ForeignKey(Word, related_name='fk_word')
    count = models.IntegerField('Count')
