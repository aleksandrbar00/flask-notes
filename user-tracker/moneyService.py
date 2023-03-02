from sqlalchemy import text
from sqlalchemy.sql import func

from db import db
from moneyTransaction import MoneyTransaction


class MoneyService:
    @staticmethod
    def add_new_transaction(user_id, payload):
        transaction = MoneyTransaction(
            description=payload['description'],
            type=payload['type'],
            amount=payload['amount'],
            user_id=user_id
        )
        db.session.add(transaction)
        db.session.commit()

    @staticmethod
    def get_period_stats(user_id, period):
        stats = dict()

        income_query = db.session.query(func.sum(MoneyTransaction.amount).label('total_income')).filter(
            db.sql.func.date(MoneyTransaction.created_at) >= period['from'],
            db.sql.func.date(MoneyTransaction.created_at) <= period['to'],
            MoneyTransaction.type == 'income',
            MoneyTransaction.user_id == user_id
        )

        expose_query = db.session.query(func.sum(MoneyTransaction.amount).label('total_expose')).filter(
            db.sql.func.date(MoneyTransaction.created_at) >= period['from'],
            db.sql.func.date(MoneyTransaction.created_at) <= period['to'],
            MoneyTransaction.type == 'expose',
            MoneyTransaction.user_id == user_id
        )

        for _res in income_query.all():
            stats['total_income'] = _res['total_income']

        for _res in expose_query.all():
            stats['total_expose'] = _res['total_expose']

        return stats

    @staticmethod
    def get_user_date_transactions(user_id, date, type='', order='created_at:desc'):
        order = order.split(':')
        order_name = order[0]
        order_dir = order[1]
        order_str = str(order_name) + " " + str(order_dir)

        query = db.session.query(MoneyTransaction).filter(
            db.sql.func.date(MoneyTransaction.created_at) == date,
            MoneyTransaction.user_id == user_id
        )

        if type:
            query = query.filter(MoneyTransaction.type == type)

        return query.order_by(text(order_str)).all()

    @staticmethod
    def edit_id_transaction(id, payload):
        transaction = db.get_or_404(MoneyTransaction, id)

        for k in payload:
            setattr(transaction, k, payload[k])

        db.session.commit()

        return '', 200
