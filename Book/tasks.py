import json
import os
from datetime import datetime
from celery import shared_task
from django.conf import settings
from .models import Author, Book, BorrowRecord
import logging


logger = logging.getLogger(__name__)

@shared_task
def generate_report():
    try:
        total_authors = Author.objects.count()
        total_books = Book.objects.count()
        borrowed_books = BorrowRecord.objects.filter(return_date__isnull=True).count()
        report_data = {
            "total_authors": total_authors,
            "total_books": total_books,
            "total_borrowed_books": borrowed_books,
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        report_filename = f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path = os.path.join(settings.REPORTS_DIR, report_filename)
        logger.info(f"Saving report to {report_path}...")
      
        with open(report_path, 'w') as report_file:
            json.dump(report_data, report_file, indent=4)
        logger.info(f"Report successfully saved as {report_filename}")
        return report_filename
    
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise e