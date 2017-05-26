def get_model_fields(model_obj):
    return set(field.name for field in model_obj._meta.get_fields())
