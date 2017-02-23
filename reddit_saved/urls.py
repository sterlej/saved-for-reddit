from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import urls

from storage import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^authorize_callback/$', views.authenticated),
    url(r'^$', views.home, name="home"),
    url(r'^', include(urls)),
    url(r'^api/', include('storage.api.urls', namespace='api')),
    url(r'^api2/', include('reddit_accounts.api.urls', namespace='api2')),
    # url(r'^search/', include('haystack.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
