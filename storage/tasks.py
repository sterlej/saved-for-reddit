from celery import task, chain, Task, group
from .models import Savable


@task
def remove_unsaved(profile_ids):
    print(Savable.objects.user_unsaved(profile_ids=profile_ids))
    return  "hello wrold"
