# project/models.py


import datetime

from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, paid=False, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
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
    tips_products = db.relationship('ProductsTips', backref='tips')

    def __repr__(self):
        return self.tip_name


class Pictures(db.Model):

    __tablename__ = 'pictures'

    picture_id = db.Column(db.Integer, primary_key=True)
    picture_name = db.Column(db.String)
    picture_url = db.Column(db.String)
    is_main = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    def __repr__(self):
        return self.picture_name


class Types(db.Model):

    __tablename__ = 'types'

    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String, nullable=False)
    type_note = db.Column(db.Text)
    parent_type_id = db.Column(db.Integer)
    product_type = db.relationship('Products', backref='types')

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
    create_time = db.Column(db.DATETIME)
    Update_time = db.Column(db.DATETIME)
    type_id = db.Column(db.Integer, db.ForeignKey('types.type_id'))
    product_pictures = db.relationship('Pictures', backref='products')
    products_tips = db.relationship('ProductsTips', backref='products')

    def __repr__(self):
        return self.product_name


class ProductsTips(db.Model):

    __tablename__ = 'products_tips'

    product_tip_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    tip_id = db.Column(db.Integer, db.ForeignKey('tips.tip_id'))

    def __repr__(self):
        return self.product_tip_id


