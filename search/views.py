from django.shortcuts import render
from django.http import HttpResponse
from storage.models import Comment


# Create your views here.
"""
What are the different facets in order to run a search.

1) Run a query with subreddit facet (May not be full word, e.g. bestof -> netflixbestof)
    - subreddit facets should be wilds cards not full text (partial index for PSql on subreddit columns&text columns)

2) Run a query with no facets
    - FT search on all text columns, number columns(Dep on query), date columns(Dep. on query)

Have a search bar, able to add facets

Facets:
    - Subreddit - Like query
    - Date
    - Title
    - Comment
"""


# QUERY = {'subreddit': 'netflix best of', 'Date': '2014', 'Title': 'underrated anime', "query 1": 'wolf children'}
# def get_query_results(request):
#     pass


def get_latest_saved(request):
    all_comments = Comment.objects.all()
    context = {
        'comments': all_comments
    }
    return render(request, 'display_saved.html', context)

get_latest_saved(None)