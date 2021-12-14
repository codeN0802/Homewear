import json
import os
import hashlib
from mysale import app
from mysale.models import *
from sqlalchemy import func
from flask_login import current_user
from sqlalchemy.sql import extract
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def read_categories():
    # return read_json(os.path.join(app.root_path,'data/categories.json'))
    return Category.query.all()

def read_prodcuts(cate_id=None, kw=None, from_price=None, to_price = None, page=1):
     # products= read_json(os.path.join(app.root_path,'data/products.json'))
     # if cate_id:
     #     products = [p for p in products if p['category_id'] == int(cate_id)]
     # if kw:
     #     products =  [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
     # if from_price:
     #     products = [p for p in products if p['price'] > float(from_price)]
     # if to_price:
     # #     products = [p for p in products if p['price'] < float(to_price)]
     products = Product.query.filter(Product.active.__eq__(True))
     if cate_id:
            products = products.filter(Product.category_id.__eq__(int(cate_id)))

     if kw:
            products = products.filter(Product.name.contains(kw))

     if from_price:
            products = products.filter(Product.price.__ge__(float(from_price)))
     if to_price:
            products = products.filter(Product.price.__le__(float(to_price)))
     page_size = app.config['PAGE_SIZE']
     start = (page-1)*page_size
     end = start+page_size
     return products.slice(start,end).all()
def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()
def count_products_cate(cate_id):
    products= Product.query.filter(Product.active.__eq__(True))
    return   products.filter(Product.category_id.__eq__(cate_id)).count()

def add_user(name,username,password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email = kwargs.get('email'),
                avatar = kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()

def check_login(username,password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_adminlogin(username,password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        admin = User.query.filter(User.user_role.__eq__("ADMIN"))
        return admin.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

#xem cate có bao nhieu sp
def product_count_by_cate():
     # products = Product.query.filter(Product.active.__eq__(True))

     return Category.query.join(Product ,(Category.id==Product.category_id) ,isouter=True).filter(Product.active.__eq__(True))\
        .add_columns(func.count(Product.id)).group_by(Category.id).all()
def count_cart(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user) # trong Receipt có thuộc tính user do backref
        db.session.add(receipt)
        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,
                              product_id= c['id'],
                              quantity = c['quantity'],
                              amount= c['price'])
            db.session.add(d)
        db.session.commit()
def count_product_stats(kw=None,from_date=None,to_date=None):

    p = db.session.query(Product.id,Product.name,
                        func.sum(ReceiptDetail.quantity * ReceiptDetail.amount))\
            .join(ReceiptDetail,(Product.id== ReceiptDetail.product_id), isouter=True)\
            .join(Receipt,(ReceiptDetail.receipt_id==Receipt.id))\
            .group_by(Product.id,Product.name)
    if kw:
        p = p.filter(Product.name.contains(kw))
    if from_date:
        p = p.filter(Receipt.created_date.__ge__(from_date))
    if to_date:
        p = p.filter(Receipt.created_date.__le__(to_date))
    return p.all()


def doanhthu(year):
    return db.session.query(extract('month', Receipt.created_date),func.sum(ReceiptDetail.quantity * ReceiptDetail.amount))\
        .join(ReceiptDetail,(Receipt.id== ReceiptDetail.receipt_id))\
        .filter(extract('year',Receipt.created_date)==year)\
        .group_by(extract('month', Receipt.created_date)).order_by(extract('month', Receipt.created_date)).all()


def get_product_by_id(product_id):
    # products = read_json(os.path.join(app.root_path,'data/products.json'))
    #
    # for p in products:
    #     if p['id'] == product_id:
    #         return p
    return Product.query.get(product_id)