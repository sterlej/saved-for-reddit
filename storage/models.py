from django.db import models
from storage.managers import SavableManager, SubredditManager
from reddit_accounts.models import RedditProfile


class Subreddit(models.Model):
    subreddit_id = models.TextField(unique=True, primary_key=True, db_index=True)
    name = models.TextField(db_index=True)

    objects = SubredditManager()


class Savable(models.Model):
    subreddit = models.ForeignKey(Subreddit, null=True)
    author_flair_text = models.TextField(null=True, blank=True)
    score = models.IntegerField(blank=True, null=True)
    created_utc = models.DateTimeField(db_index=True)
    date_saved = models.DateTimeField(db_index=True, null=True)
    author = models.TextField(null=True)
    author_user_id = models.TextField(db_index=True, unique=True, null=True)
    saved_by = models.ManyToManyField(RedditProfile, related_name="%(class)s_set")

    objects = SavableManager()

    class Meta:
        ordering = ('-created_utc',)


class Submission(Savable):
    submission_id = models.TextField(unique=True, db_index=True, primary_key=True, blank=True)
    title = models.TextField(db_index=True, null=True, blank=True)
    num_comments = models.IntegerField(null=True, blank=True)
    url = models.TextField(blank=True, null=True)
    permalink = models.TextField(blank=True, null=True)
    post_hint = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(Savable):
    comment_id = models.TextField(unique=True, db_index=True, primary_key=True, blank=True)
    # submission = models.ForeignKey(Submission, blank=True, null=True)
    body = models.TextField()
    body_html = models.TextField()
    parent_id = models.TextField(db_index=True)

    def __str__(self):
        return self.body



