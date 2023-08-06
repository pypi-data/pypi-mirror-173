
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializer import CountySerializer
from base.models import County
from rest_framework.response import Response

# Create your views here.


class BaseView(viewsets.ModelViewSet):
    queryset = County.objects.all()
    # permission_classes = [IsAuthenticated]

    @action(methods=["get", "post"], detail=False)
    def county_view(self, request):
        counties = County.objects.all()
        serializer = CountySerializer(counties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





