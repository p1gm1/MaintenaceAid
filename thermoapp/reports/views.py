#Django Rest
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import  AllowAny

# Serializer
from thermoapp.reports.serializers import ReportSerializer

class ReportViewSet(viewsets.GenericViewSet):
    """Report view set.
    
    Handles report creation, update and delete.
    """

    serializer_class = ReportSerializer

    def get_permissions(self):
        """Assign permissions based on action"""

        if self.action in ['create_report']:
            permissions = [AllowAny] #IsAuthenticated
        else:
            permissions = [AllowAny] #IsAdminUser

        return [p() for p in permissions]

    @action(detail=False, methods=['get'])
    def create_report(self, request):
        """Report creation."""
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.save()
        data = serializer.data

        return Response(data, status=status.HTTP_201_CREATED)

    
