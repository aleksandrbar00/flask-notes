from db import db

from marshmallow import Schema, fields


class MoneyTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class CreateTransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()
    type = fields.Str()
    user_id = fields.Integer()


class EditTransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()
    type = fields.Str()


class TransactionSchema(CreateTransactionSchema):
    id = fields.Integer()