from django.conf.urls import patterns, include, url
from stats import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stats.views.home', name='home'),
    # url(r'^stats/', include('stats.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # ex: /, will be redirected to /books/
    url(r'^$', views.index, name='index'),
    url(r'^books/', include('books.urls')),
)
