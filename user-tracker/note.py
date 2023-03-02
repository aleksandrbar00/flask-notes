from db import db

from marshmallow import Schema, fields


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())


class CreateNoteSchema(Schema):
    content = fields.Str()
    user_id = fields.Integer()


class NoteSchema(Schema):
    id = fields.Integer()
    content = fields.Str()
    user_id = fields.Integer()