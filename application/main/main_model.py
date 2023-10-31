from application import db


class CreditServicesTr(db.Model):
    __tablename__ = 'credit_services_tr'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }


class ServiceType(db.Model):
    __tablename__ = 'service_type'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }


class ServiceTypeOptions(db.Model):
    __tablename__ = 'service_type_options'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.engine
    }
