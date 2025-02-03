from rest_framework import status, viewsets
from rest_framework.response import Response
from core.models import BackupJob
from .serializers import BackupJobSerializer
from .tasks import backup_file
from rest_framework.permissions import IsAuthenticated

class BackupJobViewSet(viewsets.ModelViewSet):
    queryset = BackupJob.objects.all()
    serializer_class = BackupJobSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            backup_job = serializer.save(user=request.user)
            
            backup_file.delay(backup_job.id)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
