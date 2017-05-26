from haystack import indexes
from .models import Subreddit, Comment, Submission


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='comment_text.txt')
    body = indexes.CharField(model_attr='body')
    link_title = indexes.CharField(model_attr='link_title')
    savable_ptr_id = indexes.IntegerField(model_attr='savable_ptr_id')
    subreddit_id = indexes.IntegerField(model_attr='subreddit_id')
    saved_by = indexes.MultiValueField()

    def prepare_saved_by(self, obj):
        return [saved_by.id for saved_by in obj.saved_by.all()]

    def get_model(self):
        return Comment


class SubmissionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='submission_text.txt')
    title = indexes.CharField(model_attr='title')
    savable_ptr_id = indexes.IntegerField(model_attr='savable_ptr_id')
    subreddit_id = indexes.IntegerField(model_attr='subreddit_id')
    saved_by = indexes.MultiValueField()

    def prepare_saved_by(self, obj):
        return [saved_by.id for saved_by in obj.saved_by.all()]

    def get_model(self):
        return Submission

