from django.conf.urls import patterns, url
from books import views

urlpatterns = patterns('',
    # ex: /books/
    url(r'^$', views.index, name='index'),
    # ex: /books/123/
    url(r'^(?P<id>\d+)/$', views.book, name='book'),
    # ex: /books/add/
    url(r'^add/', views.add, name='add'),
)
