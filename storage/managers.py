from django.db.models.query import QuerySet
from django.db.models import Manager

import itertools


class SavableQuerySet(QuerySet):

    def all_user_savables(self, profile_ids):
        return self.filter(saved_by__in=profile_ids).distinct().prefetch_related('submission', 'comment', 'subreddit')


class SubredditQuerySet(QuerySet):

    def savable_subreddits(self, savables):
        return self.filter(subreddit_id__in=savables.values_list('subreddit_id')).distinct()


SavableManager = SavableQuerySet.as_manager
SubredditManager = SubredditQuerySet.as_manager


class ProfileManager(Manager):
    def get_all_profiles(self, local_id):
        return super(ProfileManager, self).get_queryset().filter(identity=local_id)


def get_model_fields(model_obj):
    return set(field.name for field in model_obj._meta.get_fields())


# def get_all_comments(reddit_profile_obj_seq):
#     all_comments = [prof.comment_set.all() for prof in reddit_profile_obj_seq]
#     distinct_comments = itertools.chain(*all_comments).distinct()
#     return distinct_comments
#
#
# def get_all_submissions(reddit_profile_obj_seq):
#     all_submissions = [prof.submission_set.all() for prof in reddit_profile_obj_seq]
#     distinct_submissions = itertools.chain(*all_submissions).distinct()
#     return distinct_submissions
