from . import dbase
from flask_login import UserMixin
from sqlalchemy.sql import func


# Database for User
class User(dbase.Model, UserMixin):
    id = dbase.Column(dbase.Integer, primary_key=True)
    student = dbase.Column(dbase.Integer, unique=True)
    name = dbase.Column(dbase.String(150))
    password = dbase.Column(dbase.String(150))
    products = dbase.relationship('Products', backref='owner_user')


# Database for Product
class Products(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    product_name = dbase.Column(dbase.String(150))
    product_category = dbase.Column(dbase.String(150))
    product_price = dbase.Column(dbase.Integer)
    stocklvl = dbase.Column(dbase.Integer, default=0)
    owner_id = dbase.Column(dbase.Integer, dbase.ForeignKey('user.id'))
    owner = dbase.relationship('User', backref='product_owner')


# Database for Bucket List Products
class BucketListItem(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    product_id = dbase.Column(dbase.Integer, dbase.ForeignKey('products.id'), nullable=False)
    user_id = dbase.Column(dbase.Integer, dbase.ForeignKey('user.id'), nullable=False)

    product = dbase.relationship('Products', backref='bucket_list_items')
    user = dbase.relationship('User', backref='bucket_list_items')


# Database for Liked Products
class Interest(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    product_id = dbase.Column(dbase.Integer, dbase.ForeignKey('products.id'), nullable=False)
    user_id = dbase.Column(dbase.Integer, dbase.ForeignKey('user.id'), nullable=False)

    product = dbase.relationship('Products', backref='interests')
    user = dbase.relationship('User', backref='interests')

