from django.db import models
from storage.managers import ProfileManager, SavableManager, SubredditManager


class LocalIdentity(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.id


class RedditProfile(models.Model):
    identity = models.ForeignKey(LocalIdentity, null=True) # author_id (PRAW) => user_id
    reddit_user_id = models.TextField(db_index=True, unique=True, null=True)
    username = models.TextField(unique=True, null=True) # user_name => author
    refresh_token = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)

    objects = ProfileManager()

    def update_identity(self, new_identity):
        self.identity = new_identity
        self.save()

    def __str__(self):
        return self.username


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
    #     abstract = True


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



