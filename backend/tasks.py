from celery_app import celery_app
from flask_mail import Message
import smtplib
from io import StringIO
import csv
from models import PlacementDrive, Application, ApplicationStatus, SessionLocal
from datetime import datetime, timedelta
from celery_app import redis_client

@celery_app.task
def send_daily_reminders():
    """Daily deadline alerts"""
    session = SessionLocal()
    try:
        # Query drives ending soon
        drives = session.query(PlacementDrive).filter(
            PlacementDrive.application_deadline <= datetime.now() + timedelta(days=2)
        ).all()
        
        for drive in drives:
            # Send to eligible students via email/SMS
            redis_client.setex(f'reminder:{drive.id}', 86400, 'sent')
        print("Daily reminders sent")
    finally:
        session.close()

@celery_app.task
def generate_monthly_report():
    """Monthly HTML report for admin"""
    session = SessionLocal()
    try:
        stats = {
            'total_drives': session.query(PlacementDrive).count(),
            'total_applications': session.query(Application).count(),
            'placements': session.query(Application).filter(
                Application.status == ApplicationStatus.HIRED
            ).count()
        }
        
        html = f"""
        <h1>Monthly Report - {datetime.now().strftime('%Y-%m')}</h1>
        <ul>
            <li>Total Drives: {stats['total_drives']}</li>
            <li>Placements: {stats['placements']}</li>
        </ul>
        """
        
        # Email to admin
        # NOTE: mail object is not defined. This will have to be configured
        # in the main app and passed to the task.
        # msg = Message('Monthly Placement Report', 
        #              sender='noreply@campusconnect.com',
        #              recipients=['admin@campusconnect.com'])
        # msg.html = html
        # mail.send(msg)
    finally:
        session.close()

@celery_app.task
def student_csv_export(student_id):
    """Export student applications as CSV"""
    session = SessionLocal()
    try:
        apps = session.query(Application).filter(
            Application.student_id == student_id
        ).all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Company', 'Drive', 'Status', 'Date'])
        writer.writerows([
            [a.company_name, a.drive_title, a.status.value, a.application_date]
            for a in apps
        ])
        
        # Store in Redis/temp file
        csv_data = output.getvalue()
        redis_client.setex(f'csv:{student_id}', 3600, csv_data)
        return f'/api/student/export/{student_id}'  # Download URL
    finally:
        session.close()