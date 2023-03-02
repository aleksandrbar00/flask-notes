from db import db

from marshmallow import Schema, fields


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    transactions = db.relationship('MoneyTransaction', backref='user')
    notes = db.relationship('Note', backref='user')


class CreateUserSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
