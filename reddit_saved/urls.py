"""reddit_saved URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import login, urls

from storage import views

"""
URLconf.py - simple mapping between URL patterns(regex) to python functions (views)

How django processes a request
    When a user requests a page from site, this is algo:
    1) Django determines the root URLconf module, ordinarily this is value of ROOT_URLCONF

    2) Django loads that python module and looks for the var: urlpatterns. A list of
    django.conf.urls.url() instances.

    3) Django runs through each URL pattern, stops at first run that matches requested URL

    4) When match: Django imports and calls given view, and view gets following args
        - instance of HttpRequest
        - If the matched regular expression returned no named groups, then the matches
         from the regular expression are provided as positional arguments.
"""

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', views.main_page),
    # url(r'^show_saved/$', views.get_current_saved),
    url(r'^authorize_callback/$', views.authenticated),
    # url(r'^logout/', views.logout)x
    url(r'^$', views.home, name="home"),
    url(r'^', include(urls)),
    url(r'^api/', include('storage.api.urls', namespace='api')),
    url(r'^api2/', include('reddit_accounts.api.urls', namespace='api2')),
    # url(r'^login/$', views.login, name="login"),
    # url(r'^register/$', views.register, name="register")
    # url(r'^search/', include('haystack.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
