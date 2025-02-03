from django.contrib import admin
from .models import User, BackupJob, BackupSettings

admin.site.register(User)

@admin.register(BackupJob)
class BackupJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'backup_status', 'created_at', 'completed_at')
    list_filter = ('backup_status', 'user')
    search_fields = ('user__username', 'file_name')

# Register BackupSettings model to admin panel
admin.site.register(BackupSettings)
