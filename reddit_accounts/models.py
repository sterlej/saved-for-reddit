from django.db import models
from .managers import ProfileManager
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User


class LocalIdentity(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.id)


class RedditProfile(models.Model):
    identity = models.ForeignKey(LocalIdentity, null=True) # author_id (PRAW) => user_id
    user_social = models.OneToOneField(UserSocialAuth, null=True)
    user = models.OneToOneField(User, null=True)

    objects = ProfileManager()

    def update_identity(self, new_identity):
        self.identity = new_identity
        self.save()

    def __str__(self):
        return self.user_social.__str__()