# project/models.py


import datetime

from project import db
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, paid=False, admin=False):
        self.email = email
        self.password = generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)


class Tips(db.Model):

    __tablename__ = 'tips'

    tip_id = db.Column(db.Integer, primary_key=True)
    tip_name = db.Column(db.String, nullable=False)
    tip_note = db.Column(db.Text)

    def __repr__(self):
        return self.tip_name


class Pictures(db.Model):

    __tablename__ = 'pictures'

    picture_id = db.Column(db.Integer, primary_key=True)
    picture_name = db.Column(db.String)
    picture_url = db.Column(db.String)
    product_id = db.Column(db.Integer)

    def __repr__(self):
        return self.picture_name


class Types(db.Model):

    __tablename__ = 'types'

    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String, nullable=False)
    type_note = db.Column(db.Text)
    parent_type_id = db.Column(db.Integer)

    def __repr__(self):
        return self.type_name


class Products(db.Model):

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    product_text = db.Column(db.Text)
    is_on_first = db.Column(db.Integer)
    is_rolling = db.Column(db.Integer)
    main_picture = db.Column(db.String)
    main_picture_url = db.Column(db.String)
    create_time = db.Column(db.DATETIME)
    Update_time = db.Column(db.DATETIME)
    type_id = db.Column(db.Integer)
    product_tips = db.Column(db.String)

    def query_main_products_url(self):
        obj = self.filter_by(self.is_rolling == 1).order_by(desc(self.Update_time)).limit(5).offset(0)
        return obj.main_picture_url

    def __repr__(self):
        return self.product_name


class ProductsTips(db.Model):

    __tablename__ = 'products_tips'

    product_tip_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    tip_id = db.Column(db.Integer)

    def __repr__(self):
        return self.product_tip_id


