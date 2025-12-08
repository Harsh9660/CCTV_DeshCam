from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import enum

SQLALCHEMY_DATABASE_URL = "sqlite:///./childcare_monitoring.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AlertSeverityEnum(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ZoneEnum(str, enum.Enum):
    OUTDOOR_PLAY = "outdoor_play"
    CLASSROOM = "classroom"
    STAFF_ROOM = "staff_room"
    HALLWAY = "hallway"
    ENTRANCE = "entrance"

class PersonTypeEnum(str, enum.Enum):
    STAFF = "staff"
    CHILD = "child"
    VISITOR = "visitor"
    UNKNOWN = "unknown"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    camera = Column(String, index=True)
    zone = Column(SQLEnum(ZoneEnum), index=True)
    scenario = Column(String, index=True)  # e.g., "fence_damage", "unsupervised_child"
    severity = Column(SQLEnum(AlertSeverityEnum), index=True)
    event = Column(String, index=True)
    details = Column(String)
    status = Column(String, default="Review")

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    person_type = Column(SQLEnum(PersonTypeEnum), index=True)
    face_encoding = Column(String)  # JSON string of face encoding
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    camera = Column(String, index=True)
    zone = Column(SQLEnum(ZoneEnum), index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=True)
    person_type = Column(SQLEnum(PersonTypeEnum))
    x = Column(Integer)  # Position for heatmap
    y = Column(Integer)
    activity_type = Column(String)  # e.g., "movement", "interaction"

    person = relationship("Person")

class StaffLocation(Base):
    __tablename__ = "staff_locations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    zone = Column(SQLEnum(ZoneEnum), index=True)
    duration = Column(Integer)  # seconds in this zone

    person = relationship("Person")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
