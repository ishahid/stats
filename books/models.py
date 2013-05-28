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
        list = WordCount.objects.filter(book=self).order_by('-count')[:n]
        return list

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

            s_i = int(s_i * 25)

            cloud = cloud + '<span style="font-size:' + str(s_i) + 'pt;">' + word + '</span>'
            cloud += ' '

        return mark_safe(cloud)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __unicode__(self):
        return self.title


class WordCount(models.Model):
    book = models.ForeignKey(Book, related_name='fk_book')
    word = models.ForeignKey(Word, related_name='fk_word')
    count = models.IntegerField('Count')

    def __unicode__(self):
        return self.book + '/' + self.word + '/' + self.count
