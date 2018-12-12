from flask import current_app
from sqlalchemy.sql import func
import datetime
from project import db
from marshmallow import fields, Schema


class Snake(db.Model):

    __tablename__ = 'snakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(128), unique=False, nullable=False)
    description = db.Column(db.Text, nullable=False)
    snake_genus = db.Column(db.String(128), unique=False, nullable=False)
    alive = db.Column(db.Boolean(), default=True, nullable=False)
    added_date = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.snake_genus = data.get('snake_genus')
        self.owner_id = data.get('owner_id')
        self.alive = data.get('alive')
        self.description = data.get('description')
        self.added_date = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'description': self.description,
            'snake_genus': self.snake_genus,
            'alive': self.alive,
            'added_date': self.added_date,
            'modified_at': self.modified_at
            
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = func.now()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    @staticmethod
    def get_all_snakes(owner):
        return Snake.query.filter_by(owner_id=owner)
    
    @staticmethod
    def get_one_snake(id):
        return Snake.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)
        

class SnakeSchema(Schema):
  """
  Snake Schema
  """
  id = fields.Int(dump_only=True)
  owner_id = fields.Int(required=True)
  name = fields.Str(required=True)
  description = fields.Str(required=True)
  snake_genus = fields.Str(required=True)
  alive = fields.Boolean(required=True)
  added_date = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
