from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heros'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='hero')
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def to_dict(self, include_powers=False):
        hero_dict = super().to_dict(only=('id', 'name', 'super_name'))
        
        if include_powers:
            hero_dict['powers'] =  [hero_power.power.to_dict() for hero_power in self.hero_powers]
            
        return hero_dict
    
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='power')
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('description')
    def validate_description(self, key, desc):
        if len(desc) < 20:
            raise ValueError("Description should be at least 20 characters")
        
        return desc
    
    def to_dict(self):
        return super().to_dict(only=('id','name','description'))
    
class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    
    hero_id = db.Column(db.Integer, db.ForeignKey('heros.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates('strength')
    def validates_strength(self, key, strength):
        if strength not in ['Strong','Weak','Average']:
            raise ValueError("Strength must be either Strong, Weak or Average")

        return strength