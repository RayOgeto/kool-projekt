from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Need(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # food, clothing, shelter, medical, education, etc.
    urgency_level = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    status = db.Column(db.String(20), default='active')  # active, fulfilled, cancelled
    amount_needed = db.Column(db.Float, nullable=True)  # for monetary needs
    unit = db.Column(db.String(50), nullable=True)  # kg, pieces, etc.
    location = db.Column(db.String(200), nullable=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    donations = db.relationship('Donation', backref='need', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'urgency_level': self.urgency_level,
            'status': self.status,
            'amount_needed': self.amount_needed,
            'unit': self.unit,
            'location': self.location,
            'recipient_id': self.recipient_id,
            'recipient_name': f"{self.recipient.first_name} {self.recipient.last_name}" if self.recipient else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Need {self.title}>' 