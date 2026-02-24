from enum import Enum as pyEnum
from sqlalchemy import Enum, create_engine, Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime




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
    REJECTED = 'REJECTED'



class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(Enum(UserRole), default = UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    is_blacklisted = Column(Boolean, default=False)

    # Relationships
    company = relationship('CompanyProfile', backref='user', uselist=False)
    student = relationship('StudentProfile', backref='user', uselist=False)


class CompanyProfile(Base):
    __tablename__ = 'company_profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    company_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    hr_contact = Column(String(100))
    approval_status = Column(Enum(CompanyApprovalStatus), default=CompanyApprovalStatus.PENDING)


class StudentProfile(Base):
    __tablename__ = 'student_profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    roll_no = Column(String(50), unique=True)  # Changed from usn
    branch = Column(String(50), nullable=True) # make nullable
    cgpa = Column(Float, nullable=True) # make nullable
    graduation_year = Column(Integer, nullable=True) # make nullable
    skills = Column(Text, nullable=True)  # make nullable
    avatar_url = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)


class PlacementDrive(Base):
    __tablename__ = 'placement_drives'
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('company_profiles.user_id'), nullable=False)
    company_name = Column(String(100), nullable=False)
    job_title = Column(String(100), nullable=False)
    job_description = Column(Text, nullable=False)
    salary = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)

    # flattened eligibility
    eligibility_branch = Column(String(200), nullable=False)
    eligibility_min_cgpa = Column(Float, nullable=False)
    eligibility_year = Column(Integer, nullable=False)

    application_deadline = Column(DateTime, nullable=False)
    status = Column(Enum(DriveStatus), default=DriveStatus.PENDING)
    created_at = Column(DateTime, default=func.now())

    applications = relationship('Application', backref='drive', lazy=True)
    company = relationship('CompanyProfile', backref='placement_drives')




class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student_profiles.user_id'), nullable=False)
    student_name = Column(String(100), nullable=False)  # denormalized
    drive_id = Column(Integer, ForeignKey('placement_drives.id'), nullable=False)
    drive_title = Column(String(100), nullable=False)
    company_name = Column(String(100), nullable=False)
    application_date = Column(DateTime, nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False)

    
class PlacementStat(Base):
    __tablename__ = 'placement_stats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_students = Column(Integer, default=0, nullable=False)
    total_companies = Column(Integer, default=0, nullable=False)
    total_drives = Column(Integer, default=0, nullable=False)
    total_placements = Column(Integer, default=0, nullable=False)


# Export engine for use in other modules
engine = create_engine('sqlite:///campus_connect.db')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)