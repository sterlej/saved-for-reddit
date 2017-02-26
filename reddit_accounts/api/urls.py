from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profiles/$',
        views.RedditProfileListView.as_view(),
        name='profiles_list'),

    url(r'^authenticate/$',
        views.RedditProfileListView.as_view(),
        name='authenticate'),

    url(r'^register/$',
        views.RedditProfileCreateView.as_view(),
        name='register'),
]