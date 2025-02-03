import shutil
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from core.models import BackupJob
import os

def send_backup_notification(backup_job, status):
    subject = f"Backup Status: {status}"
    message = f"Your backup job for {backup_job.file_name} is {status}."
    send_mail(subject, message, settings.EMAIL_HOST_USER, [backup_job.user.email])

@shared_task(bind=True)
def backup_file(self, backup_job_id):
    try:
        backup_job = BackupJob.objects.get(id=backup_job_id)
        backup_job.update_status('in_progress')

        source_path = os.path.join(settings.MEDIA_ROOT, 'uploads', backup_job.file_name)
        destination_path = os.path.join(settings.MEDIA_ROOT, 'backups', backup_job.file_name)

        shutil.copyfile(source_path, destination_path)

        backup_job.backup_path = destination_path
        backup_job.update_status('completed')
        send_backup_notification(backup_job, 'completed')

        return f"Backup of file {backup_job.file_name} completed successfully."

    except Exception as e:
        backup_job.update_status('failed')
        send_backup_notification(backup_job, 'failed')
        return f"Backup of file {backup_job.file_name} failed with error: {str(e)}."
