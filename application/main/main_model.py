from application import db


class CreditCashTr(db.Model):
    __tablename__ = 'credit_cash_tr'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }
