from rest_framework import serializers
from core.models import BackupJob

class BackupJobSerializer(serializers.ModelSerializer):
    model = BackupJob
    fields = '__all__'