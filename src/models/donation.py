from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=True)  # kg, pieces, etc.
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, delivered, cancelled
    donation_type = db.Column(db.String(50), nullable=False)  # monetary, goods, services
    need_id = db.Column(db.Integer, db.ForeignKey('need.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields for delivery
    delivery_address = db.Column(db.String(200), nullable=True)
    delivery_instructions = db.Column(db.Text, nullable=True)
    delivery_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'unit': self.unit,
            'description': self.description,
            'status': self.status,
            'donation_type': self.donation_type,
            'need_id': self.need_id,
            'donor_id': self.donor_id,
            'donor_name': f"{self.donor.first_name} {self.donor.last_name}" if self.donor else None,
            'need_title': self.need.title if self.need else None,
            'delivery_address': self.delivery_address,
            'delivery_instructions': self.delivery_instructions,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Donation {self.id} - {self.amount} {self.unit}>' 