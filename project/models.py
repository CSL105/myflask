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


class ProductPictures(db.Model):

    __tablename__ = 'product_pictures'

    picture_id = db.Column(db.Integer, primary_key=True)
    picture_name = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    def __repr__(self):
        return self.picture_name


class Products(db.Model):

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    product_text = db.Column(db.String)
    is_on_first = db.Column(db.Integer)
    is_rolling = db.Column(db.Integer)
    main_picture = db.Column(db.String)
    create_time = db.Column(db.DATETIME)
    Update_time = db.Column(db.DATETIME)
    product_pictures = db.relationship('ProductPictures', backref=db.backref('products'))

    def __repr__(self):
        return self.product_name


class Tips(db.Model):

    __tablename__ = 'tips'

    tip_id = db.Column(db.Integer, primary_key=True)
    tip_name = db.Column(db.String, nullable=False)
    tip_note = db.Column(db.String)

    def __repr__(self):
        return self.tip_name

