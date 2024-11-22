from django.core.management import call_command


# def ti_management_backup():
#     try:
#         call_command('dbbackup')
#         call_command('mediabackup')
#     except:
#         pass

import logging

from datetime import timedelta
from django.utils.timezone import now
from django.core.management import call_command
from django.core.management.base import CommandError
from TI_Management_app.models import DocumentsDatabase, RegisterRelief, SignatureRelief

# Configure logging
logger = logging.getLogger(__name__)

def ti_management_backup():
    try:
        # Backup database
        logger.info("Starting database backup...")
        call_command('dbbackup')
        logger.info("Database backup completed successfully.")

        # Backup media
        logger.info("Starting media backup...")
        call_command('mediabackup')
        logger.info("Media backup completed successfully.")

        # Cleanup old signature images
        logger.info("Starting cleanup of old signature images...")
        old_documents = DocumentsDatabase.objects.filter(
            created_date__lt=now() - timedelta(hours=1),  # only 1 hour !!!!
            signature_image__isnull=False
        )
        deleted_count = 0
        for document in old_documents:
            # Delete the associated signature image file from storage
            if document.signature_image:
                document.signature_image.delete(save=False)
            document.signature_image = None
            document.save()
            deleted_count += 1
        logger.info(f"Removed signature images from {deleted_count} old documents.")



        # # Cleanup old signature images
        # logger.info("Starting cleanup of old signature images...")
        # old_documents = RegisterRelief.objects.filter(
        #     created_date__lt=now() - timedelta(days=1),
        #     signature_image__isnull=False
        # )
        # deleted_count = 0
        # for document in old_documents:
        #     # Delete the associated signature image file from storage
        #     if document.signature_image:
        #         document.signature_image.delete(save=False)
        #     document.signature_image = None
        #     document.save()
        #     deleted_count += 1
        # logger.info(f"Removed signature images from {deleted_count} old documents.")
        #
        #
        #
        # # Cleanup old signature images
        # logger.info("Starting cleanup of old signature images...")
        # old_documents = SignatureRelief.objects.filter(
        #     created_date__lt=now() - timedelta(days=1),
        #     signature_image__isnull=False
        # )
        # deleted_count = 0
        # for document in old_documents:
        #     # Delete the associated signature image file from storage
        #     if document.signature_image:
        #         document.signature_image.delete(save=False)
        #     document.signature_image = None
        #     document.save()
        #     deleted_count += 1
        # logger.info(f"Removed signature images from {deleted_count} old documents.")

    except CommandError as e:
        logger.error(f"Backup command failed: {e}")
    except Exception as e:
        logger.exception("An unexpected error occurred during the backup or cleanup process.")


