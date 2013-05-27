from django.db import models
from django.db.models import Sum


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
