# from django.utils import timezone
# import datetime
# from haystack import indexes
# from storage.models import Comment
#
# """
# ============================================================
# SearchIndex API
# ===
# SearchIndex class allows way to provide data to backend
# in structured format
#
# Background - Unlike relational dbs, SE supported by haystack
# are mostly doc-based.
#
#     The schema used by most SE is the same for all types of
#     data added
#         -More of a key-value store
#
# Significance of document=True - all engines have a min of
# data they need to function
#
#     At least 1 field must be specified as document=True
#
# Stored/Indexed Fields - When retrieving search results, will
# likely have to access the obj in the db
#
#     This can hit the db heavily
#         - ex: .get(pk=result.id) per object, if search is
#         popular -> performance hit
#             - 2 way to prevent:
#
#             1) SearchQuerySet.load_all, which tries to group
#             all simil objs and pull them through one query
#             instead of many
#
#             2) Leverage stored fields. By default, all fields
#             in haystack are indexed and stored. By using a
#             stored field, can store common used data in a way
#             that you don't need to hit db, when processing
#             search result
#
#             -One great way to levarge is in pre-rendering an
#             objs search results template DURING indexing. Def
#             an additional field, render template with it, and
#             it follows the main indexed record into the index.
#
# Keeping the index fresh
#
#     Conventional method is to use SearchIndex in combination
#     with cron.
#
#     RealtimeSignalProcessor - Used django's signals to
#     immediately update index any time a model is saved/deleted
#         - elasticsearch & solr are the only SE's that handles this
#         well under load - even then make sure server capacity to
#         spare -
#
#     A third option is to develop a custom QueuedSignalProcessor
#     that, much like RealtimeSignalProcessor, uses Django’s
#     signals to enqueue messages for updates/deletes. Then
#     writing a management command to consume these messages in
#     batches, yielding a nice compromise between the previous
#     two options.
#
# Advanced Data Preparation
#
#     model_attr - Allows you to easily get data from a Django
#     model to the document in your index - it hadles direct attr
#     access and callable functions within your model
#
#     For more control, SearchIndex objects have a 'preparation' stage that
#     populates data just before it is indexed
#
#         - loosely follows django's forms
#         - makes data more friendly to the backend
#         - prepare_'field'
# """
#
# class CommentIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     comment_id = indexes.CharField(model_attr='comment_id')
#     subreddit_id = indexes.CharField(model_attr='subreddit_id')
#     subreddit = indexes.CharField(model_attr='subreddit')
#     link_title = indexes.CharField(model_attr='link_title')
#     body = indexes.CharField(model_attr='body')
#     author = indexes.CharField(model_attr='author')
#     created_utc = indexes.DateTimeField(model_attr='created_utc')
#     date_stored = indexes.DateTimeField(model_attr='date_stored')
#
#     def get_model(self):
#         return Comment
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.filter(date_stored__lte=timezone.now())
#
#
#
