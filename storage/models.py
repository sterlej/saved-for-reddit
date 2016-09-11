from django.db import models


class Comment(models.Model):
    link_author = models.CharField(max_length=100)
    subreddit_id = models.CharField(max_length=100,
                                    unique=True,
                                    blank=False,
                                    null=False,
                                    db_index=True)
    comment_id = models.CharField(max_length=100,
                          unique=True,
                          blank=False,
                          null=False,
                          db_index=True)
    subreddit = models.CharField(max_length=100,
                                 blank=False,
                                 null=False,
                                 db_index=True)
    author_flair_text = models.CharField(max_length=100)
    score = models.IntegerField(blank=False,
                                null=False)
    link_title = models.CharField(max_length=100,
                                  db_index=True,
                                  null=False,
                                  blank=False)
    link_id = models.CharField(max_length=100,
                               db_index=True,
                               null=False,
                               blank=False)
    body = models.TextField(db_index=True,
                            blank=False,
                            null=False)
    body_html = models.TextField(blank=False,
                                 null=False)
    author = models.CharField(max_length=100,
                              blank=False,
                              null=False,
                              db_index=True)
    created_utc = models.DateTimeField(blank=False,
                                       null=False,
                                       db_index=True)
    link_url = models.URLField()
    parent_id = models.CharField(db_index=True,
                                 max_length=100)
    date_stored = models.DateTimeField(blank=False,
                                       null=False,
                                       db_index=True)