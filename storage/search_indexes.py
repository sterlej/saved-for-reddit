from haystack import indexes
from .models import Subreddit, Comment, Submission


# class SubredditIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True)
#     name = indexes.CharField(model_attr='name')
#
#     def get_model(self):
#         return Subreddit

    # def index_queryset(self, using=None):
    #     return self.get_model().objects.all()


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='comment_text.txt')
    body = indexes.CharField(model_attr='body')
    link_title = indexes.CharField(model_attr='link_title')
    savable_ptr_id = indexes.IntegerField(model_attr='savable_ptr_id')

    def get_model(self):
        return Comment

    # def index_queryset(self, using=None):
    #     return self.get_model().objects.all()


class SubmissionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='submission_text.txt')
    title = indexes.CharField(model_attr='title')
    savable_ptr_id = indexes.IntegerField(model_attr='savable_ptr_id')

    def get_model(self):
        return Submission

    # def index_queryset(self, using=None):
    #     return self.get_model().objects.all()



