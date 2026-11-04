from datetime import datetime
import numpy as np
from database.db import db

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships with explicit primaryjoin to bind to unique student_id
    embeddings = db.relationship(
        'FaceEmbedding',
        backref='student',
        cascade='all, delete-orphan',
        lazy=True,
        foreign_keys='FaceEmbedding.student_id',
        primaryjoin='Student.student_id == FaceEmbedding.student_id'
    )
    attendance_records = db.relationship(
        'Attendance',
        backref='student',
        cascade='all, delete-orphan',
        lazy=True,
        foreign_keys='Attendance.student_id',
        primaryjoin='Student.student_id == Attendance.student_id'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'registered_at': self.registered_at.strftime('%Y-%m-%d %H:%M:%S') if self.registered_at else ""
        }


class FaceEmbedding(db.Model):
    __tablename__ = 'face_embeddings'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    embedding = db.Column(db.LargeBinary, nullable=False)  # Serialized numpy array
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_embedding(self, embedding_array: np.ndarray):
        """Serializes the numpy float32 array to binary bytes."""
        if embedding_array is None:
            self.embedding = b''
            return
        arr = np.asarray(embedding_array, dtype=np.float32).flatten()
        self.embedding = arr.tobytes()

    def get_embedding(self) -> np.ndarray:
        """Deserializes the binary bytes back into a numpy float32 array of shape (128,)."""
        if not self.embedding:
            return np.zeros(128, dtype=np.float32)
        return np.frombuffer(self.embedding, dtype=np.float32)


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(50), nullable=False, default='Present')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.student.name if self.student else "Unknown",
            'department': self.student.department if self.student else "Unknown",
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else "",
            'status': self.status
        }
