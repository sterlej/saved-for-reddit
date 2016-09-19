from django.db import models


class Comment(models.Model):
    link_author = models.CharField(max_length=100, blank=True,null=True)
    subreddit_id = models.CharField(max_length=100, unique=True, db_index=True)
    comment_id = models.CharField(max_length=100, unique=True, db_index=True)
    subreddit = models.CharField(max_length=100, db_index=True)
    author_flair_text = models.CharField(max_length=100, null=True, blank=True)
    score = models.IntegerField()
    link_title = models.CharField(max_length=100, db_index=True,)
    link_id = models.CharField(max_length=100, db_index=True)
    body = models.TextField()
    body_html = models.TextField()
    author = models.CharField(max_length=100, db_index=True)
    created_utc = models.DateTimeField(db_index=True)
    link_url = models.URLField()
    parent_id = models.CharField(db_index=True, max_length=100)
    date_stored = models.DateTimeField(db_index=True)

    def __unicode__(self):
        return self.body