"""
When to use service

1. External service w/ model
2. Helper tasks not touching DB!!
3. Short lived obj w.o. DB state
4. Long running celery tasks

-Should be stateless
"""


def get_subset_of_dict(dictionary_obj, subset_fields_seq):
    return {k: dictionary_obj[k] for k in subset_fields_seq}


def create_model_row_from_dict(model_object, dictionary_object, id_field):
    model_row, created = model_object.objects.get_or_create(pk=dictionary_object[id_field],
                                                            defaults=dictionary_object)
    return model_row





