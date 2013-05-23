from django.db import models

class Word(models.Model):
    text  = models.CharField('Text', max_length=100, unique=True)
    
    def __unicode__(self):
        return self.text
    
    class Meta:
        verbose_name        = 'word'
        verbose_name_plural = 'words'

class Book(models.Model):
    title     = models.CharField('Title', max_length=255, unique=True)
    author    = models.CharField('Author', max_length=255)
    published = models.CharField('Published', max_length=255, null=True, blank=True)
    
    def get_unique_words(self):
        "Returns list of unique words in this book."
        return []

    def _get_total_words_count(self):
        "Returns count of total words in this book."
        return 0
    total_words = property(_get_total_words_count)

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name        = 'book'
        verbose_name_plural = 'books'

class WordCount(models.Model):
    book  = models.ForeignKey(Book, related_name='fk_book')
    word  = models.ForeignKey(Word, related_name='fk_word')
    count = models.IntegerField('Count')
