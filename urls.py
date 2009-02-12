from django.conf.urls.defaults import *
from views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^f15/', include('f15.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
	(r'^$', index),
	(r'^m/?$', mobile),
	(r'^sitemap.xml$', sitemap),
	(r'search', redirect_to_search),
	(r'^fetch', fetch_tweets),
	(r'^tweets/(\d+)$', tweet),
	(r'^tweets/first$', first),
	(r'', not_found),
)
