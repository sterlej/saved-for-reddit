from django.db import models
from storage.managers import SavableManager, SubredditManager
from reddit_accounts.models import RedditProfile
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User


class Subreddit(models.Model):
    # subreddit_id = models.TextField(unique=True, primary_key=True, db_index=True)
    name = models.TextField(db_index=True)

    objects = SubredditManager()


class Savable(models.Model):
    subreddit = models.ForeignKey(Subreddit, null=True)
    author_flair_text = models.TextField(null=True, blank=True)
    score = models.IntegerField(blank=True, null=True)
    created_utc = models.DateTimeField(db_index=True, null=True)
    date_saved = models.DateTimeField(db_index=True, null=True)
    author = models.TextField(null=True)
    author_user_id = models.TextField(db_index=True, null=True)
    saved_by = models.ManyToManyField(User, related_name="%(class)s_set")
    is_saved = models.BooleanField(default=True)

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
    thumbnail = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(Savable):
    comment_id = models.TextField(unique=True, db_index=True, primary_key=True, blank=True)
    # submission = models.ForeignKey(Submission, blank=True, null=True)
    link_author = models.TextField(null=True, blank=True)
    body = models.TextField(blank=True, null=True)
    body_html = models.TextField(blank=True, null=True)
    parent_id = models.TextField(db_index=True, blank=True, null=True)
    link_url = models.TextField(blank=True, null=True)
    link_title = models.TextField(db_index=True, blank=True, null=True)
    permalink = models.TextField(blank=True, null=True)

    @property
    def full_comments_url(self):
        return '/'.join(self.permalink.split('/')[:-1])

    def __str__(self):
        return self.body



