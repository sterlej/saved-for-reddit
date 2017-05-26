from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$',
        views.SavableListView.as_view(),
        name='saved_list'),

    url(r'^subreddits$',
        views.SubredditListView.as_view(),
        name='subreddits'),

    url(r'^comments/create$',
        views.CommentCreateView.as_view(),
        name='comments_create'),

    url(r'^submissions/create$',
        views.SubmissionCreateView.as_view(),
        name='submissions_create'),

    url(r'^delete/(?P<pk>[0-9]+)$',
        views.SavableDetailView.as_view(),
        name='delete'),

    url(r'^search',
        views.SavableSearchView.as_view(),
        name='search-savable'),
]