from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'souk.core.views.home', name='home'),
    url(r'^me/$', 'souk.core.views.me', name='me'),
    url(r'^balance/$', 'souk.core.views.balance', name='balance'),
    url(r'^address/$', 'souk.core.views.address', name='address'),
    url(r'^nest$', 'souk.core.views.nest', name='nest'),
    url(r'^items/new$', 'souk.core.views.new_item', name='new_item'),
    url(r'^request/(?P<item_id>\d+)/$', 'souk.core.views.request_item', name='request_item'),
    url(r'^request/(?P<item_id>\d+)/confirm/$', 'souk.core.views.request_item_confirm', name='request_item_confirm'),

    url(r'^borrowed/$', 'souk.core.views.borrowed', name='borrowed'),
    url(r'^return/(?P<item_id>\d+)/$', 'souk.core.views.return_item', name='return_item'),

    url(r'^requests/$', 'souk.core.views.list_requests', name='list_requests'),
    url(r'^requests/(?P<req_id>\d+)/accept/$', 'souk.core.views.accept_request', name='accept_request'),

    url(r'^backlog$', 'souk.core.views.backlog', name='backlog'),

    # url(r'^souk/', include('souk.foo.urls')),


    url(r'^search/$', 'souk.core.views.search', name='search'),
    url(r'^craigslist/$', 'souk.core.views.craigslist', name='craigslist'),
    url(r'^craigslist/submit/$', 'souk.core.views.cragslist_submit', name='cragslist_submit'),
    url(r'^craigslist/submit/(?P<req_id>\d+)/$', 'souk.core.views.craigslist_reply', name='craigslist_reply'),

    url(r'^accept/(?P<req_id>\d+)/(?P<hash>\w+)/$', 'souk.core.views.craigslist_accept', name='craigslist_reply'),
    url(r'^accept/(?P<req_id>\d+)/(?P<hash>\w+)/done$', 'souk.core.views.craigslist_accept_done', name='craigslist_reply'),

    url(r'^login/$', 'django.contrib.auth.views.login',name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {"next_page" : reverse_lazy('login')}, name="logout"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social'))
)
