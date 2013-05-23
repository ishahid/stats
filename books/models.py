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
    
    def get_unique_words_count(self):
        """Returns count of unique words in this book."""
        return WordCount.objects.filter(book=self).count()

    def get_total_words_count(self):
        """Returns count of total words in this book."""
        list = WordCount.objects.filter(book=self)
        count = 0
        for wc in list:
            count = count + wc.count;

        return count

    def get_top_twenty_words(self):
        """Returns top twenty words in this book."""
        list = WordCount.objects.filter(book=self).order_by('-count')[:20]
        return list

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name        = 'book'
        verbose_name_plural = 'books'

class WordCount(models.Model):
    book  = models.ForeignKey(Book, related_name='fk_book')
    word  = models.ForeignKey(Word, related_name='fk_word')
    count = models.IntegerField('Count')

    def __unicode__(self):
        return self.word.text + ' [' + self.count + ']'
