from django.db.models.query import QuerySet


class SavableQuerySet(QuerySet):

    def user_unsaved(self, profile_ids):
        return self.filter(saved_by__in=profile_ids).distinct().filter(is_saved=False)

    def all_user_savables(self, profile_ids):
        return self.filter(saved_by__in=profile_ids).distinct().filter(is_saved=True).prefetch_related('submission',
                                                                                                       'comment',
                                                                                                       'subreddit',
                                                                                                       'saved_by')
    def all_prefetch(self):
        return self.all().prefetch_related('submission', 'comment', 'subreddit', 'saved_by')


class SubredditQuerySet(QuerySet):

    def savable_subreddits(self, savables):
        return self.filter(subreddit_id__in=savables.values_list('id')).distinct()


SavableManager = SavableQuerySet.as_manager
SubredditManager = SubredditQuerySet.as_manager
