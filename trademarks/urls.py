from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from trademarks import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^search$', views.search, name='search'),
    #url(r'^search_sortbymatch$', views.search_sortbymatch, name='search_sortbymatch'),
    url(r'^load_more$', views.load_more, name='load_more'),
)
