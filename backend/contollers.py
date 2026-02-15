from flask_restful import Resource, reqparse
from flask import request, session
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import ApplicationStatus, Base, Users, UserRole,CompanyApprovalStatus,DriveStatus, CompanyProfile, StudentProfile, PlacementDrive, Application, PlacementStat
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from datetime import datetime





def is_admin():
    identify = get_jwt_identity()
    user = session.query(Users).filter_by(id=identify).first()
    return bool(user and user.role == UserRole.Admin)




class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role= data.get('role', UserRole.STUDENT) # default to student if not provided

        if not all ([name,email,password]):
            return {"message": "Name, email and password are required"}, 400
        

        #check if email already exists
        existing = session.query(Users).filter_by(email=email).first()
        if existing:
            return {"message": 'User already exists'},400
        
        new_user = Users(name=name, email=email, password=password, role=role)
        session.add(new_user)
        session.commit()
        return {"message": "User registered successfully"}, 201
    


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {"message": 'Missing credentials'},400
        
        user = Users.query.filter_by(email=email).first()

        if not user or user.password != password:
            return {"message": "invalid email or password"}, 401
        
        token = create_access_token(identity = user.id)

        return{
            "message":"login successful",
            "access_token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        },200
    



# admin apis

class CompainesList(Resource):
    @jwt_required()
    def get(self):
        # admin check
        if not is_admin():
            return {"message": "Admin access required"}, 403
        
        compaines= session.query(CompanyProfile).join(Users).filter(Users.role == UserRole.COMPANY, Users.is_active==True).all()
        return{
            'compaines':[{
                'id': c.id,
                'company_name':c.company_name,
                'email': c.user.email,
                'hr_contact': c.hr_contact,
                'approval_status': c.approval_status
            } for c in compaines]
        }, 200

# class ComapnyApprove(Resource):
#     @jwt_required()
#     def post(self, company_id):
#         if not is_admin():
#             return {"message": "Admin access required"}, 403
        
#         company = session.query(CompanyProfile).get(company_id)
#         if company and company.approval_status == CompanyApprovalStatus.PENDING:
#             company.approval_status = CompanyApprovalStatus.APPROVED
#             session.commit()
#             return {"message": "Company approved successfully"}, 200
#         return {'error': 'not found'}, 404
    

# class ComapanyReject(Resource):
#     @jwt_required()
#     def post(self, company_id):
#         if not is_admin():
#             return {"message": "Admin access required"}, 403
#         company = session.query(CompanyProfile).get(company_id)
#         if company and company.approval_status == CompanyApprovalStatus.PENDING:
#             company.approval_status = CompanyApprovalStatus.REJECTED
#             session.commit()
#             return {"message": "Company rejected successfully"}, 200


class CompanyStatus(Resource):
    @jwt_required()
    def post(self, company_id):
        status = request.json.get('status')
        company = session.query(CompanyProfile).get(company_id)
        if company and status in [CompanyApprovalStatus.PENDING, CompanyApprovalStatus.APPROVED, CompanyApprovalStatus.REJECTED]:
            company.approval_status = status
            session.commit()
            return{'message': f'company status updated to {status}'},200
        return {'error': 'not found or invalid status'},404
    

class DrivesList(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {'message': 'admin access required'},403
        drives = session.query(PlacementDrive).all()
        return {
            'drives': [{
                'id': d.id,
                'title': d.title,
                'description': d.description,
                'company': d.company.company_name if d.company else None,
                'deadline': d.deadline
            } for d in drives]
        },200
    
class DriveStatus(Resource):
    @jwt_required()
    def post(self, drive_id):
        status = request.json.get('status')
        drive = session.query(PlacementDrive).get(drive_id)
        if drive and status in [DriveStatus.PENDING, DriveStatus.ACTIVE, DriveStatus.CLOSED, DriveStatus.REJECTED]:
            drive.status = status
            session.commit()
            return {'message': f'Drive status updated to {status}'},200
        return {'error': 'not found or invalid status'},404



class StudentList(Resource):
    @jwt_required()
    def get(self):
        # admin check
        if not is_admin():
            return {"message": "Admin access required"}, 403
        
        students= session.query(StudentProfile).join(Users).filter(Users.role == UserRole.STUDENT).all()
        return{
            'students':[{
                'id': c.id,
                'name': c.user.name,
                'email': c.user.email,
                'cgpa': c.user.cgpa,
                'branch': c.branch,
                'graduation_year': c.graduation_year,
                'skills': c.skills,
                'is_blacklisted': c.user.is_blacklisted,
                'is_active': c.user.is_active
            } for c in students]
        }, 200

class UserBlacklist(Resource):
    @jwt_required()
    def post(self, user_id):
        if not is_admin():
            return {'message': 'admin access required'}, 403
        user = session.query(Users).get(user_id)
        if user and user.role == UserRole.STUDENT:
            user.is_blacklisted = not user.is_blacklisted
            user.is_active = not user.is_blacklisted 
            session.commit()
            status = 'blacklisted' if user.is_blacklisted else 'activated'
            return {'message': f'user {status} '},200

class AdminStats(Resource):
    @jwt_required()
    def get(self):
        return{
            'total_students': session.query(Users).filter_by(role=UserRole.STUDENT).count(),
            'total_companies': session.query(Users).filter_by(role=UserRole.COMPANY).count(),
            'active_companies': session.query(Users).filter_by(role=UserRole.COMPANY, is_active=True).count(),
            'pending_companies': session.query(CompanyProfile).filter_by(approval_status=CompanyApprovalStatus.PENDING).count(),
            'total_drives': session.query(PlacementDrive).count(),
            'active_drives': session.query(PlacementDrive).filter_by(status=DriveStatus.ACTIVE).count(),
            'placements': session.query(PlacementStat).count()
        }
    

class AdminSearch(Resource):

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q',type=str,required=True)
        parser.add_argument("type", type= str, choices=['students', 'companies'], required= True)
        args = parser.parse_args()

        if args['type'] == 'students':
            results = session.query(Users, StudentProfile).outerjoin(StudentProfile, Users.id == StudentProfile.id).filter(or_(Users.name.ilike(f'%{args['q']}%'), Users.email.ilike(f'%{args['q']}%'))).limit(20).all()
        else:
            results = session.query(Users, CompanyProfile).outerjoin(CompanyProfile, Users.id == CompanyProfile.id).filter(or_(Users.name.ilike(f'%{args['q']}%'), Users.email.ilike(f'%{args['q']}%'))).limit(20).all()
        return {
            'results': [{
                'id': r[0].id,
                'name': r[0].name,
                'email': r[0].email,
                'role': r[0].role,
                'details': {
                    'company_name': r[1].company_name if args['type'] == 'companies' else None,
                    'hr_contact': r[1].hr_contact if args['type'] == 'companies' else None,
                    'approval_status': r[1].approval_status if args['type'] == 'companies' else None,
                    'branch': r[1].branch if args['type'] == 'students' else None,
                    'cgpa': r[1].cgpa if args['type'] == 'students' else None,
                    'graduation_year': r[1].graduation_year if args['type'] == 'students' else None,
                    'skills': r[1].skills if args['type'] == 'students' else None
                }
            } for r in results]
        }
    


class CompanyProfile(Resource):
    @jwt_required()
    def get(self):
        user_id  = get_jwt_identity()
        company = session.query(CompanyProfile).filter(CompanyProfile.id == Users.id, Users.role == UserRole.COMPANY).first()
        if not company or company.approval_status != CompanyApprovalStatus.APPROVED:
            return {'message':'Company profile not found or not approved'},403
        return{
            'id' : company.id,
            'company_name': company.company_name,
            'email': company.user.email,
            'hr_contact': company.hr_contact,
            'approval_status': company.approval_status,
            'description': company.description
        }
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('company_name', type = str)
        parser.add_argument('hr_contact')
        parser.add_argument('description')
        args = parser.parse_args()


        company = session.query(CompanyProfile),filter(CompanyProfile.id == user_id, CompanyProfile.approval_status == CompanyApprovalStatus.APPROVED).first()

        if company:
            for key, value in args.items():
                if value is not None:
                    setattr(company, key, value)
            session.commit()
            return {'message': 'profile updated'}, 200
        return {'message': 'company not approved'},403
    

class CompanyDrives(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        company = session.query(CompanyProfile).filter(CompanyProfile.id == user_id, CompanyProfile.approval_status == CompanyApprovalStatus.APPROVED).first()

        if not company:
            return {'error': 'company not approved'}, 403
        

        parser = reqparse.RequestParser()
        parser.add_argument('job_title', required = True)
        parser.add_argument('job_description', required = True)
        parser.add_argument('eligibility_branch', required= True)
        parser.add_argument('eligibility_min_cgpa',type = float, required= True)
        parser.add_argument('eligibility_year', type = float, required= True)
        parser.add_argument('application_deadline', required= True)
        args = parser.parse_args()

        drive = PlacementDrive(
            company_id = company.id,
            company_name = company.company_name,
            job_title = args['job_title'],
            job_description = args['job_description'],
            eligibility_branch = args['eligibility_branch'],
            eligibility_min_cgpa = args['eligibility_min_cgpa'],
            eligibility_year = args['eligibility_year'],
            application_deadline = args['application_deadline'],
            status = DriveStatus.PENDING,
            created_at = datetime.utcnow()
        )
        session.add(drive)
        session.commit()
        return {'message': 'drive created and pending approval', 'drive_id': drive.id}, 201
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        drives = session.query(PlacementDrive).filter(PlacementDrive.company_id == user_id).all()
        return {
            'drives':[{
                'id': d.id,
                'tittle': d.job_title,
                'status': d.status,
                'deadline': d.application_deadline.isoformat(),
                'applications_count': session.query(Application).filter(Application.drive_id == d.id).count()
            } for d in drives]

        }
    

class CompanyDriveApplicaitons(Resource):
    @jwt_required()
    def get(self, drive_id):
        user_id = get_jwt_identity()
        drive = session.query(PlacementDrive).filter(PlacementDrive.id == drive_id, PlacementDrive.company_id == user_id).first()
        if not drive:
            return {'message': 'drive not found'}, 404
        apps = session.query(Application).filter(Application.drive_id == drive_id).all()
        return {
            'applications': [{
                'id': a.id,
                'student_name': a.student_name,
                'application_date': a.application_date.isoformat(),
                'status': a.status
            } for a in apps]
        }
    

class CompanyApplicationStatus(Resource):
    @jwt_required()
    def post(self, application_id):
        user_id = get_jwt_identity()
        app = session.query(Application).join(PlacementDrive).filter(Application.id == application_id, PlacementDrive.company_id == user_id).first()
        if not app:
            return {'message': 'application not found'}, 404
        status = request.json.get('status')
        if status not in [ApplicationStatus.APPLIED, ApplicationStatus.SHORTLISTED, ApplicationStatus.REJECTED]:
            return {'message': 'invalid status'}, 400
        app.status = status
        session.commit()
        return {'message': f'application status updated to {status}'},200
    

class StudentProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        student = session.query(StudentProfile).filter(StudentProfile.id == user_id).first()
        if not student:
            return {'message': 'student profile not found'}, 404
        return {
            'id': student.id,
            'name': student.user.name,
            'email': student.user.email,
            'branch': student.branch,
            'cgpa': student.cgpa,
            'graduation_year': student.graduation_year,
            'skills': student.skills
        }
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('branch', type = str)
        parser.add_argument('cgpa', type = float)
        parser.add_argument('graduation_year', type = int)
        parser.add_argument('skills', type = str)
        args = parser.parse_args()

        student = session.query(StudentProfile).filter(StudentProfile.id == user_id).first()
        if student:
            for key, value in args.items():
                if value is not None:
                    setattr(student, key, value)
            session.commit()
            return {'message': 'profile updated'}, 200
        else: 
            new_student = StudentProfile(id=user_id, **args)
            session.add(new_student)
            session.commit()
        return {'message': 'profile created'}, 201
    

class StudentDrives(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        student = session.query(StudentProfile).filter(StudentProfile.id == user_id).first()
        if not student:
            return {'message': 'student profile not found'}, 404
        
        drives = session.query(PlacementDrive).filter(
            PlacementDrive.eligibility_branch.ilike(f'%{student.branch}%'),
            PlacementDrive.eligibility_min_cgpa <= student.cgpa,
            PlacementDrive.eligibility_year <= student.graduation_year,
            PlacementDrive.status == DriveStatus.ACTIVE
        ).all()

        return {
            'drives': [{
                'id': d.id,
                'title': d.job_title,
                'company': d.company_name,
                'deadline': d.application_deadline.isoformat(),
                'status': d.status
            } for d in drives]
        }   
    

class StudentApply(Resource):
    @jwt_required()
    def post(self, drive_id):
        user_id = get_jwt_identity()
        student = session.query(StudentProfile).filter(StudentProfile.id == user_id).first()
        if not student:
            return {'message': 'student profile not found'}, 404
        
        drive = session.query(PlacementDrive).filter(PlacementDrive.id == drive_id, PlacementDrive.status == DriveStatus.ACTIVE).first()
        if not drive:
            return {'message': 'drive not found or not active'}, 404
        
        existing_app = session.query(Application).filter(Application.student_id == user_id, Application.drive_id == drive_id).first()
        if existing_app:
            return {'message': 'already applied to this drive'}, 400
        
        app = Application(
            student_id = user_id,
            student_name = student.user.name,
            drive_id = drive.id,
            drive_title = drive.job_title,
            company_name = drive.company_name,
            application_date = datetime.utcnow(),
            status = ApplicationStatus.APPLIED
        )
        session.add(app)
        session.commit()
        return {'message': 'application submitted successfully'}, 201   
    

class StudentApplications(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        apps = session.query(Application).filter(Application.student_id == user_id).all()
        return {
            'applications': [{
                'id': a.id,
                'drive_title': a.drive_title,
                'company_name': a.company_name,
                'application_date': a.application_date.isoformat(),
                'status': a.status
            } for a in apps]
        }
