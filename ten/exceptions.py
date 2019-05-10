# Doc: https://docs.djangoproject.com/en/2.1/_modules/django/core/exceptions/

class NotActivateTenant(Exception):
    '''There is no active tenant'''
    pass


class OrphanTenant(Exception):
    pass