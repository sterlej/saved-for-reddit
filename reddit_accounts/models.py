from django.db import models
from .managers import ProfileManager


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