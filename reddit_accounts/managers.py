from django.db.models.query import QuerySet


class ProfileQuerySet(QuerySet):

    def get_all_profiles(self, local_id):
        return self.filter(identity=local_id)


ProfileManager = ProfileQuerySet.as_manager
