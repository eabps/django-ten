from rest_framework.exceptions import APIException


# https://www.django-rest-framework.org/api-guide/exceptions/#apiexception
class TenantNotDefined(APIException):
    status_code = 406
    default_detail = 'Tenant not defined. To access this resource it is necessary to activate a tenant'
    default_code = 'tenant_not_defined'