# Doc: https://docs.djangoproject.com/en/2.1/_modules/django/core/exceptions/

class NotActivateTenant(Exception):
    pass


class OrphanTenant(Exception):
    pass