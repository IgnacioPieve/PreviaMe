import functools
from firebase_admin import auth


def assert_fields(request, required, optional=None):
    if optional is None:
        optional = []
    missing_fields = []
    final_dict = {}
    for required_field in required:
        if required_field not in request:
            missing_fields.append(required_field)
        else:
            final_dict[required_field] = request[required_field]

    if len(missing_fields) > 0:
        return False, {
            'error': 'Missing required fields',
            'fields': missing_fields
        }
    for optional_field in optional:
        if optional_field in request:
            final_dict[optional_field] = request[optional_field]
    return True, final_dict
