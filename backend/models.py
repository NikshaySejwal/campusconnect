from flask_sqlalchemy import SQlAlchemy
from enum import Enum as pyEnum
from sqlalchemy import Enum
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, func




Base = declarative_base()

class UserRole(pyEnum):
    Admin = 'ADMIN'
    COMPANY = 'COMPANY'
    STUDENT = 'STUDENT'


class CompanyApprovalStatus(pyEnum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class DriveStatus(pyEnum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    CLOSED = 'CLOSED'
    REJECTED = 'REJECTED'

class ApplicationStatus(pyEnum):
    APPLIED = 'APPLIED'
    SHORTLISTED = 'SHORTLISTED'
    SELECTED = 'SELECTED'
    REJCTED = 'REJECTED'



class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), default = UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    is_blacklisted = Column (Boolean, default=False)

    # Relationships
    comapny = relationship('ComapnyProfile', backref='user', uselist=False)
    student = relationship('StudentProfile', backref='user', uselist = False)


class CompanyProfile(Base):
    __tablename__ = 'company_profiles'
    id = Column(Integer, ForeignKey('user.id'),  primary_key=True)
    company_name = Column(String(100), nullable = False)
    hr_contact = Column(String(100))
    approval_status = Column(Enum(CompanyApprovalStatus), default= CompanyApprovalStatus.PENDING)


class StudentProfile(Base):
    __tablename__ = 'student_profiles'
    id = Column(Integer, ForeignKey('user.id'),  primary_key=True)
    branch = Column(String(50), nullable = False)
    cgpa = Column (Float, nullable=False)
    graduation_year = Column(Integer)
    skills = Column(Text) #Json String or comma-separeted 

    user = relationship('Application', backref= 'student', lazy =True)


class PlacementDrive(Base):
    __tablename__ = 'palcement_drives'
    id = Column(Integer, primary_key= True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('CompanyProfile.id'), nullable= False)
    company_name = Column(String(100), nullable=False)
    job_tittle = Column(String(100),nullable=False)
    job_description = Column(Text,nullable=False)

    # flattened eligibility 
    eligibility_branch = Column (String(200), nullable= False)
    eligibility_min_cgpa = Column(Float, nullable=False)
    eligibility_year= Column(Integer , nullable=False)


    application_deadline = Column(datetime, nullable = False)
    status = Column(Enum(DriveStatus), default = DriveStatus.PENDING)
    created_at = Column(DateTime, default = func.now())

    application = relationship('Application', backref= 'drive', lazy= True)
    company = relationship('CompanyProfile', backref= 'PlacementDrive')




class Application(Base):
    __tablename__ = 'applications'
    id = Column (Integer, primary_key=True,autoincrement= True)
    student_id= Column(Integer, ForeignKey('StudentProfile.id'), nullable= False)
    student_name = Column(String(100), nullable= False)  #denormalized
    drive_id= Column (Integer, ForeignKey('PlacementDrive.id'), nullable= False)
    drive_title = Column(String, nullable=False)
    company_name = Column (String, nullable= False)
    application_date = Column (datetime,nullable= False)
    status = Column(Enum(ApplicationStatus), default = ApplicationStatus.APPLIED, nullable= False)

    
class PlacementStat(Base):
    __tablename__ = 'placement_stat'
    id = Column (Integer, nullable = False)
    total_student = Column (Integer, default= 0 , nullable= False)
    total_compaines= Column (Integer, default= 0 , nullable= False)
    total_drive= Column (Integer,default= 0 , nullable= False)
    total_placement= Column(Integer, default=0, nullable= False)