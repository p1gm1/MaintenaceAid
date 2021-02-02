#Standard libraries
import hashlib
from datetime import datetime

#Django Rest
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import  AllowAny

# Serializer
#from thermoapp.reports.serializers import ReportSerializer

#AWS
from thermoapp.utils.storages import upload_to_aws

#Model Report
from thermoapp.reports.models import Report

class ReportViewSet(viewsets.GenericViewSet):
    """Report view set.

    Handles report creation, update and delete.
    """

    #serializer_class = ReportSerializer

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
        #serializer = ReportSerializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
        #data = serializer.data
        data = []

        return Response(data, status=status.HTTP_201_CREATED)

#/new_report
def new_report(request):

    if request.method == 'POST':
        #Create a random string to rename the picture
        string = str(datetime.now())
        new_string = hashlib.sha256(string.encode()).hexdigest()
        # Get image name
        img = request.FILES['image']
        #split image name in name & extension
        complement, ext = img.name.split('.')
        #Change image name to a new string & extension
        img.name = new_string + '.' + ext

        # storage image to aws
        upload_to_aws(img)

        #Create new object in db Image
        new_report = Report.objects.create()

        # Get aws bucket url
        # BUCKET_URL =

        #title of new image into bucket URL
        bucket_url = BUCKET_URL + img.name

        #Set public id
        new_report.public_id = new_string
        #Set user
        # new_report.user =
        #set components
        new_report.component = request.FILES['component']
        #Set details
        new_report.detail = request.FILES['detail']
        #Set actions
        new_report.action = request.FILES['action']
        #Set bucket_url
        new_report.bucket_url = bucket_url

        #Save the new report
        new_report.save()

        context = {'success' : 'Report was succesfully upload'}
        return redirect('/')
    else:
        context = {}
        return render(request, 'base/home.html', context)
