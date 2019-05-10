from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from test_ten.models import ScheduledService
from .serializers import ScheduledServiceSerializer


class ScheduledServiceViewSet(ModelViewSet):
    #queryset = TouristSpot.objects.all()
    serializer_class = ScheduledServiceSerializer
    #authentication_classes = (TokenAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        date = self.request.query_params.get('date')
        #city = self.request.query_params.get('city')

        queryset = ScheduledService.objects.all()
        
        if date:
            queryset = queryset.filter(date__iexact=date)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        return super(ScheduledServiceViewSet, self).create(request, *args, **kwargs)