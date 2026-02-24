
from flask_restful import Resource, reqparse
from flask import request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import ApplicationStatus, Base, Users, UserRole, CompanyApprovalStatus, DriveStatus, CompanyProfile, StudentProfile, PlacementDrive, Application, PlacementStat
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
from celery_app import redis_client
from tasks import student_csv_export

# Initialize database session (use the same engine/session as models.py)
from models import engine
Session = sessionmaker(bind=engine)
db = Session()


def is_admin():
    identify = int(get_jwt_identity())
    user = db.query(Users).filter_by(id=identify).first()
    return bool(user and user.role == UserRole.Admin)


class PublicDrivesResource(Resource):
    def get(self):
        drives = db.query(PlacementDrive).filter(PlacementDrive.status == DriveStatus.APPROVED).all()
        return {
            'drives': [{
                'id': d.id,
                'title': d.job_title,
                'company': d.company_name,
                'deadline': d.application_deadline.isoformat() if isinstance(d.application_deadline, datetime) else str(d.application_deadline),
            } for d in drives]
        }, 200

class PublicDriveResource(Resource):
    def get(self, drive_id):
        drive = db.query(PlacementDrive).get(drive_id)
        if not drive or drive.status != DriveStatus.APPROVED:
            return {'message': 'drive not found or not active'}, 404
        return {
            'id': drive.id,
            'title': drive.job_title,
            'company': drive.company_name,
            'description': drive.job_description,
            'deadline': drive.application_deadline.isoformat() if isinstance(drive.application_deadline, datetime) else str(drive.application_deadline),
            'branch': drive.eligibility_branch,
            'cgpa': drive.eligibility_min_cgpa,
            'salary': drive.salary,
            'location': drive.location
        }, 200


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'STUDENT')

        if not all([name, email, password]):
            return {"message": "Name, email and password are required"}, 400

        if db.query(Users).filter_by(email=email).first():
            return {"message": 'User with this email already exists'}, 400

        # Handle Student Registration
        if role == 'STUDENT':
            usn = data.get('usn')
            department = data.get('department')
            if not usn or not department:
                return {"message": "USN and department are required for students"}, 400
            if db.query(StudentProfile).filter_by(roll_no=usn).first():
                return {"message": 'A student with this USN already exists'}, 400

            # All validation passed, create user and profile
            new_user = Users(name=name, email=email, password=password, role=UserRole.STUDENT)
            db.add(new_user)
            db.flush()
            profile = StudentProfile(user_id=new_user.id, roll_no=usn, branch=department)
            db.add(profile)
            db.commit()

            # Create token for auto-login
            token = create_access_token(identity=str(new_user.id))
            return {
                "message": "Student registered successfully",
                "access_token": token,
                "user": {
                    "id": new_user.id,
                    "name": new_user.name,
                    "email": new_user.email,
                    "role": new_user.role.value
                }
            }, 201

        # Handle Company Registration
        elif role == 'COMPANY':
            company_name = data.get('company_name')
            if not company_name:
                return {"message": "Company name is required"}, 400

            # All validation passed, create user and profile
            new_user = Users(name=name, email=email, password=password, role=UserRole.COMPANY)
            db.add(new_user)
            db.flush()
            profile = CompanyProfile(user_id=new_user.id, company_name=company_name)
            db.add(profile)
            db.commit()

            return {"message": "Company registration submitted for approval."}, 201

        else:
            return {"message": "Invalid role specified"}, 400


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {"message": 'Missing credentials'}, 400
        
        user = db.query(Users).filter_by(email=email).first()

        if not user or user.password != password:
            return {"message": "invalid email or password"}, 401
        
        if user.is_blacklisted:
            return {"message": "Your account has been suspended."}, 403
        
        token = create_access_token(identity=str(user.id))

        return {
            "message": "login successful",
            "access_token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.value
            }
        }, 200



# admin apis
class AdminCompanyResource(Resource):
    @jwt_required()
    def get(self, company_id):
        if not is_admin():
            return {"message": "Admin access required"}, 403
        
        company = db.query(CompanyProfile).filter(CompanyProfile.user_id == company_id).first()
        if not company:
            return {'message': 'Company profile not found'}, 404

        drives = db.query(PlacementDrive).filter(PlacementDrive.company_id == company.user_id).all()
        
        return {
            'id': company.user_id,
            'company_name': company.company_name,
            'email': company.user.email,
            'hr_contact': company.hr_contact,
            'approval_status': company.approval_status.value,
            'description': company.description,
            'drives': [{
                'id': d.id,
                'title': d.job_title,
                'status': d.status.value,
                'deadline': d.application_deadline.isoformat() if isinstance(d.application_deadline, datetime) else str(d.application_deadline),
            } for d in drives]
        }, 200

class AdminDriveResource(Resource):
    @jwt_required()
    def get(self, drive_id):
        if not is_admin():
            return {'message': 'admin access required'}, 403
        drive = db.query(PlacementDrive).get(drive_id)
        if not drive:
            return {'message': 'drive not found'}, 404
        return {
            'id': drive.id,
            'title': drive.job_title,
            'company': drive.company_name,
            'description': drive.job_description,
            'deadline': drive.application_deadline.isoformat() if isinstance(drive.application_deadline, datetime) else str(drive.application_deadline),
            'branch': drive.eligibility_branch,
            'cgpa': drive.eligibility_min_cgpa,
            'salary': drive.salary,
            'location': drive.location
        }, 200


class CompaniesList(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {"message": "Admin access required"}, 403
        
        companies = db.query(CompanyProfile).join(Users).filter(Users.role == UserRole.COMPANY, Users.is_active == True).all()
        return {
            'companies': [{
                'id': c.user_id,
                'company_name': c.company_name,
                'email': c.user.email,
                'hr_contact': c.hr_contact,
                'approval_status': c.approval_status.value
            } for c in companies]
        }, 200


class CompanyStatusResource(Resource):
    @jwt_required()
    def post(self, company_id):
        status = request.json.get('status')
        company = db.query(CompanyProfile).filter_by(user_id=company_id).first()
        if company and status in [e.value for e in CompanyApprovalStatus]:
            company.approval_status = CompanyApprovalStatus[status]
            db.commit()
            return {'message': f'company status updated to {status}'}, 200
        return {'error': 'not found or invalid status'}, 404
    

class DrivesListResource(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {'message': 'admin access required'}, 403
        drives = db.query(PlacementDrive).all()
        return {
            'drives': [{
                'id': d.id,
                'title': d.job_title,
                'company': d.company_name,
                'deadline': d.application_deadline.isoformat() if isinstance(d.application_deadline, datetime) else str(d.application_deadline),
                'status': d.status.value
            } for d in drives]
        }, 200
    
class DriveStatusResource(Resource):
    @jwt_required()
    def post(self, drive_id):
        status = request.json.get('status')
        drive = db.query(PlacementDrive).get(drive_id)
        if drive and status in [e.value for e in DriveStatus]:
            drive.status = DriveStatus[status]
            db.commit()
            return {'message': f'Drive status updated to {status}'}, 200
        return {'error': 'not found or invalid status'}, 404



class StudentListResource(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {"message": "Admin access required"}, 403
        
        students = db.query(StudentProfile).join(Users).filter(Users.role == UserRole.STUDENT).all()
        return {
            'students': [{
                'id': c.user_id,
                'name': c.user.name,
                'email': c.user.email,
                'cgpa': c.cgpa,
                'branch': c.branch,
                'graduation_year': c.graduation_year,
                'skills': c.skills,
                'is_blacklisted': c.user.is_blacklisted,
                'is_active': c.user.is_active
            } for c in students]
        }, 200

class UserBlacklistResource(Resource):
    @jwt_required()
    def post(self, user_id):
        if not is_admin():
            return {'message': 'admin access required'}, 403
        user = db.query(Users).get(user_id)
        if user and user.role == UserRole.STUDENT:
            user.is_blacklisted = not user.is_blacklisted
            user.is_active = not user.is_blacklisted 
            db.commit()
            status = 'blacklisted' if user.is_blacklisted else 'activated'
            return {'message': f'user {status}'}, 200
        return {'error': 'user not found or not a student'}, 404

class AdminStatsResource(Resource):
    @jwt_required()
    def get(self):
        return {
            'total_students': db.query(Users).filter_by(role=UserRole.STUDENT).count(),
            'total_companies': db.query(Users).filter_by(role=UserRole.COMPANY).count(),
            'active_companies': db.query(Users).filter_by(role=UserRole.COMPANY, is_active=True).count(),
            'pending_companies': db.query(CompanyProfile).filter_by(approval_status=CompanyApprovalStatus.PENDING).count(),
            'total_drives': db.query(PlacementDrive).count(),
            'active_drives': db.query(PlacementDrive).filter_by(status=DriveStatus.APPROVED).count(),
            'placements': db.query(PlacementStat).count()
        }, 200
    

class AdminSearchResource(Resource):

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=True)
        parser.add_argument("type", type=str, choices=['students', 'companies'], required=True)
        args = parser.parse_args()

        if args['type'] == 'students':
            results = db.query(Users, StudentProfile).outerjoin(StudentProfile, Users.id == StudentProfile.user_id).filter(or_(Users.name.ilike(f'%{args["q"]}%'), Users.email.ilike(f'%{args["q"]}%'))).limit(20).all()
        else:
            results = db.query(Users, CompanyProfile).outerjoin(CompanyProfile, Users.id == CompanyProfile.user_id).filter(or_(Users.name.ilike(f'%{args["q"]}%'), Users.email.ilike(f'%{args["q"]}%'))).limit(20).all()
        return {
            'results': [{
                'id': r[0].id,
                'name': r[0].name,
                'email': r[0].email,
                'role': r[0].role.value,
                'details': {
                    'company_name': r[1].company_name if args['type'] == 'companies' and r[1] else None,
                    'hr_contact': r[1].hr_contact if args['type'] == 'companies' and r[1] else None,
                    'approval_status': r[1].approval_status.value if args['type'] == 'companies' and r[1] else None,
                    'branch': r[1].branch if args['type'] == 'students' and r[1] else None,
                    'cgpa': r[1].cgpa if args['type'] == 'students' and r[1] else None,
                    'graduation_year': r[1].graduation_year if args['type'] == 'students' and r[1] else None,
                    'skills': r[1].skills if args['type'] == 'students' and r[1] else None
                }
            } for r in results]
        }, 200
    


class CompanyProfileResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        company = db.query(CompanyProfile).filter(CompanyProfile.user_id == user_id).first()
        if not company:
            return {'message': 'Company profile not found'}, 404
        return {
            'id': company.user_id,
            'company_name': company.company_name,
            'email': company.user.email,
            'hr_contact': company.hr_contact,
            'approval_status': company.approval_status.value,
            'description': company.description
        }, 200
    
    @jwt_required()
    def put(self):
        user_id = int(get_jwt_identity())
        parser = reqparse.RequestParser()
        parser.add_argument('company_name', type=str)
        parser.add_argument('hr_contact')
        parser.add_argument('description')
        args = parser.parse_args()

        company = db.query(CompanyProfile).filter(CompanyProfile.user_id == user_id, CompanyProfile.approval_status == CompanyApprovalStatus.APPROVED).first()

        if company:
            for key, value in args.items():
                if value is not None:
                    setattr(company, key, value)
            db.commit()
            return {'message': 'profile updated'}, 200
        return {'message': 'company not approved'}, 403
    

class CompanyDrivesResource(Resource):
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        company = db.query(CompanyProfile).filter(CompanyProfile.user_id == user_id, CompanyProfile.approval_status == CompanyApprovalStatus.APPROVED).first()

        if not company:
            return {'error': 'company not approved'}, 403
        

        parser = reqparse.RequestParser()
        parser.add_argument('job_title', required=True)
        parser.add_argument('job_description', required=True)
        parser.add_argument('eligibility_branch', required=True)
        parser.add_argument('eligibility_min_cgpa', type=float, required=True)
        parser.add_argument('eligibility_year', type=int, required=True)
        parser.add_argument('application_deadline', required=True)
        parser.add_argument('salary', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()

        drive = PlacementDrive(
            company_id=company.user_id,
            company_name=company.company_name,
            job_title=args['job_title'],
            job_description=args['job_description'],
            eligibility_branch=args['eligibility_branch'],
            eligibility_min_cgpa=args['eligibility_min_cgpa'],
            eligibility_year=args['eligibility_year'],
            application_deadline=datetime.fromisoformat(args['application_deadline']),
            status=DriveStatus.PENDING,
            created_at=datetime.utcnow(),
            salary=args['salary'],
            location=args['location']
        )
        db.add(drive)
        db.commit()
        return {'message': 'drive created and pending approval', 'drive_id': drive.id}, 201
    
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        drives = db.query(PlacementDrive).filter(PlacementDrive.company_id == user_id).all()
        return {
            'drives': [{
                'id': d.id,
                'title': d.job_title,
                'status': d.status.value,
                'deadline': d.application_deadline.isoformat() if isinstance(d.application_deadline, datetime) else str(d.application_deadline),
                'applications_count': db.query(Application).filter(Application.drive_id == d.id).count()
            } for d in drives]

        }, 200
    

class CompanyDriveApplicationsResource(Resource):
    @jwt_required()
    def get(self, drive_id):
        user_id = int(get_jwt_identity())
        drive = db.query(PlacementDrive).filter(PlacementDrive.id == drive_id, PlacementDrive.company_id == user_id).first()
        if not drive:
            return {'message': 'drive not found'}, 404
        apps = db.query(Application).filter(Application.drive_id == drive_id).all()
        return {
            'applications': [{
                'id': a.id,
                'student_id': a.student_id,
                'student_name': a.student_name,
                'application_date': a.application_date.isoformat() if isinstance(a.application_date, datetime) else str(a.application_date),
                'status': a.status.value
            } for a in apps]
        }, 200
    

class CompanyApplicationStatusResource(Resource):
    @jwt_required()
    def post(self, application_id):
        user_id = int(get_jwt_identity())
        app = db.query(Application).join(PlacementDrive).filter(Application.id == application_id, PlacementDrive.company_id == user_id).first()
        if not app:
            return {'message': 'application not found'}, 404
        
        status = request.json.get('status')
        if not status or status not in [e.value for e in ApplicationStatus]:
            return {'message': 'Invalid status provided'}, 400

        new_status = ApplicationStatus[status]

        if new_status == ApplicationStatus.HIRED:
            student_id = app.student_id
            
            # Check if student is already placed
            already_placed = db.query(PlacementStat).filter_by(student_id=student_id).first()
            if already_placed:
                return {'message': 'This student has already been recorded as placed.'}, 400

            app.status = ApplicationStatus.HIRED
            drive = db.query(PlacementDrive).get(app.drive_id)

            new_placement = PlacementStat(
                student_id=student_id,
                drive_id=app.drive_id,
                company_name=drive.company_name,
                salary=drive.salary,
                placement_date=datetime.utcnow()
            )
            db.add(new_placement)

            db.query(Application).filter(
                Application.student_id == student_id,
                Application.id != application_id,
                or_(
                    Application.status == ApplicationStatus.APPLIED,
                    Application.status == ApplicationStatus.SHORTLISTED
                )
            ).update({'status': ApplicationStatus.REJECTED})

            db.commit()
            return {'message': 'Student hired successfully. A placement record has been created and other applications have been rejected.'}, 200
        else:
            app.status = new_status
            db.commit()
            return {'message': f'Application status updated to {status}'}, 200
    
class StudentProfileViewResource(Resource):
    @jwt_required()
    def get(self, student_id):
        user_id = int(get_jwt_identity())
        user = db.query(Users).filter(Users.id == user_id).first()

        if not user or (user.role not in [UserRole.Admin, UserRole.COMPANY]):
            return {'message': 'Unauthorized'}, 403

        student = db.query(StudentProfile).filter(StudentProfile.user_id == student_id).first()
        if not student:
            return {'message': 'student profile not found'}, 404
        return {
            'id': student.user_id,
            'name': student.user.name,
            'email': student.user.email,
            'branch': student.branch,
            'cgpa': student.cgpa,
            'graduation_year': student.graduation_year,
            'skills': student.skills,
            'bio': getattr(student, 'bio', ''),
            'avatar_url': getattr(student, 'avatar_url', None)
        }, 200

class StudentProfileResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        student = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
        if not student:
            return {'message': 'student profile not found'}, 404
        return {
            'id': student.user_id,
            'name': student.user.name,
            'email': student.user.email,
            'branch': student.branch,
            'cgpa': student.cgpa,
            'graduation_year': student.graduation_year,
            'skills': student.skills,
            'bio': getattr(student, 'bio', ''),
            'avatar_url': getattr(student, 'avatar_url', None)
        }, 200
    
    @jwt_required()
    def put(self):
        user_id = int(get_jwt_identity())
        parser = reqparse.RequestParser()
        parser.add_argument('branch', type=str)
        parser.add_argument('cgpa', type=float)
        parser.add_argument('graduation_year', type=int)
        parser.add_argument('skills', type=str)
        parser.add_argument('bio', type=str)
        args = parser.parse_args()

        student = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
        if student:
            for key, value in args.items():
                if value is not None:
                    setattr(student, key, value)
            db.commit()
            return {'message': 'profile updated'}, 200
        else: 
            return {'message': 'Student profile not found'}, 404
    

class StudentDrivesResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        student = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
        if not student:
            return {'message': 'Student profile not found'}, 404

        # Dynamically build the query
        query = db.query(PlacementDrive).filter(PlacementDrive.status == DriveStatus.APPROVED)

        if student.branch:
            query = query.filter(PlacementDrive.eligibility_branch.ilike(f'%{student.branch}%'))
        if student.cgpa is not None:
            query = query.filter(PlacementDrive.eligibility_min_cgpa <= student.cgpa)
        if student.graduation_year:
            query = query.filter(PlacementDrive.eligibility_year <= student.graduation_year)

        drives = query.all()

        result = {
            'drives': [{
                'id': d.id,
                'title': d.job_title,
                'company': d.company_name,
                'deadline': d.application_deadline.isoformat() if isinstance(d.application_deadline, datetime) else str(d.application_deadline),
                'status': d.status.value,
                'salary': d.salary,
                'location': d.location
            } for d in drives]
        }
        
        return result, 200
    

class StudentApplyResource(Resource):
    @jwt_required()
    def post(self, drive_id):
        user_id = int(get_jwt_identity())
        user = db.query(Users).get(user_id)
        student = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()

        if not student or not user:
            return {'message': 'Student profile not found'}, 404
        
        drive = db.query(PlacementDrive).filter(PlacementDrive.id == drive_id, PlacementDrive.status == DriveStatus.APPROVED).first()
        if not drive:
            return {'message': 'drive not found or not active'}, 404

        # Security: Re-validate eligibility before allowing to apply
        if not (
            student.branch and drive.eligibility_branch and student.branch.lower() in drive.eligibility_branch.lower() and
            student.cgpa and drive.eligibility_min_cgpa and student.cgpa >= drive.eligibility_min_cgpa and
            student.graduation_year and drive.eligibility_year and student.graduation_year == drive.eligibility_year
        ):
            return {'message': 'You do not meet the eligibility criteria for this drive.'}, 403

        existing_app = db.query(Application).filter(Application.student_id == user_id, Application.drive_id == drive_id).first()
        if existing_app:
            return {'message': 'already applied to this drive'}, 400
        
        app = Application(
            student_id=user_id,
            student_name=user.name,
            drive_id=drive.id,
            drive_title=drive.job_title,
            company_name=drive.company_name,
            application_date=datetime.utcnow(),
            status=ApplicationStatus.APPLIED
        )
        db.add(app)
        db.commit()
        return {'message': 'application submitted successfully'}, 201   
    

class StudentApplicationsResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        apps = db.query(Application).filter(Application.student_id == user_id).all()
        return {
            'applications': [{
                'id': a.id,
                'drive_title': a.drive_title,
                'company_name': a.company_name,
                'application_date': a.application_date.isoformat() if isinstance(a.application_date, datetime) else str(a.application_date),
                'status': a.status.value
            } for a in apps]
        }, 200


class StudentExportResource(Resource):
    @jwt_required()
    def post(self):
        """Initiates the CSV export task for the logged-in student."""
        user_id = int(get_jwt_identity())
        task = student_csv_export.delay(user_id)
        return {'task_id': task.id}, 202

    @jwt_required()
    def get(self):
        """Downloads the exported CSV for the logged-in student."""
        user_id = int(get_jwt_identity())
        csv_data = redis_client.get(f'csv:{user_id}')
        if csv_data:
            return Response(
                csv_data,
                mimetype="text/csv",
                headers={"Content-disposition":
                         "attachment; filename=application_history.csv"}
            )
        else:
            return {'message': 'Export not found or not ready. Please initiate the export first.'}, 404
