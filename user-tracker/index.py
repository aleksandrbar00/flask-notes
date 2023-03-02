import os
from flask import Flask, jsonify, request
from authService import AuthService
from noteService import NoteService
from note import CreateNoteSchema, NoteSchema
from userService import UserService
from user import UserSchema, CreateUserSchema
from moneyService import MoneyService
from moneyTransaction import CreateTransactionSchema, TransactionSchema, EditTransactionSchema
from datetime import date
from db import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

userService = UserService()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI", '')
app.config['JWT_SECRET_KEY'] = os.environ.get("SECRET_KEY", '')

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/user/<int:user_id>')
@jwt_required()
def get_user_info(user_id):
    schema = UserSchema()
    return jsonify(schema.dump(userService.get_user_info(user_id)))


@app.route('/user', methods=['POST'])
def add_new_user():
    payload = CreateUserSchema().load(request.get_json())
    userService.create(payload)
    return '', 204


@app.route('/get_day_incomes')
@jwt_required()
def get_day_incomes():
    schema = TransactionSchema(many=True)
    return jsonify(schema.dump(MoneyService.get_user_date_transactions(get_jwt_identity(), date.today(),
                                                                       request.args.get('type'),
                                                                       request.args.get('order'))))


@app.route('/day_stats')
@jwt_required()
def get_day_stats():
    period = {
        'from': request.args.get('period_from'),
        'to': request.args.get('period_to')
    }
    return jsonify(MoneyService.get_period_stats(get_jwt_identity(), period)), 200


@app.route('/transactions/', methods=['POST'])
@jwt_required()
def add_day_income():
    payload = CreateTransactionSchema().load(request.get_json())
    MoneyService.add_new_transaction(get_jwt_identity(), payload)
    return '', 204


@app.route('/transactions/<int:transaction_id>/edit', methods=['PUT'])
@jwt_required()
def edit_id_transaction(transaction_id):
    payload = EditTransactionSchema().load(request.get_json(), partial=True)
    return MoneyService.edit_id_transaction(transaction_id, payload)


@app.route('/auth/login', methods=['POST'])
def login_user():
    return AuthService.login_user(request.get_json())


@app.route('/notes', methods=['GET'])
@jwt_required()
def add_user_note():
    schema = NoteSchema(many=True)
    period = {
        'from': request.args.get('period_from'),
        'to': request.args.get('period_to')
    }
    return jsonify(schema.dump(NoteService.get_user_notes(get_jwt_identity(), period))), 200


@app.route('/notes', methods=['POST'])
@jwt_required()
def get_user_notes():
    payload = CreateNoteSchema().load(request.get_json())
    NoteService.add_note(get_jwt_identity(), payload['content'])
    return '', 201

