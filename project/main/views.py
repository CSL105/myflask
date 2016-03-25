# coding:utf-8
# project/main/views.py


#################
#### imports ####
#################

from flask.ext.login import login_required
from flask import render_template, Blueprint, url_for, redirect, flash, request
from project.models import Tips, Types, Products, ProductsTips, Pictures
from project import db
from project.furniture.views import get_nav_types
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists
from sqlalchemy import desc
import os

basedir = os.path.basename(os.path.dirname(__file__))

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################
'''
@main_blueprint.route('/')
def home():
    return render_template('main/index.html')
'''


@main_blueprint.route('/')
def home():
    # 获取滚动图片及产品id
    main_picture_urls = []
    main_picture_products = db.session.query(Products).filter(Products.is_rolling == 1).order_by(
        desc(Products.Update_time)).limit(5).offset(0)
    for main_product in main_picture_products:
        main_picture_urls.append((main_product.main_picture_url, main_product.product_id))
    rolling_num = len(main_picture_urls)
    # 获取各类型下需要展示的图片及产品id
    types_products = []
    types = db.session.query(Types).filter().order_by(Types.type_id).all()
    for this_type in types:
        type_products = db.session.query(Products).filter(Products.type_id == this_type.type_id and
                                                          Products.is_on_first == 1).order_by(
            desc(Products.Update_time)).limit(6).offset(0)
        for product in type_products:
            types_products.append((this_type.type_id, this_type.type_name,
                                   product.product_id, product.main_picture_url,
                                   product.product_name, product.product_text))

    return render_template('main/index.html', main_picture_urls=main_picture_urls, rolling_num=rolling_num,
                           types=types, types_products=types_products, nav_types=get_nav_types())


@main_blueprint.route('/this_type/<int:type_id>')
def this_type(type_id):
    this_one_type = db.session.query(Types).filter(Types.type_id==type_id).all()

    products = db.session.query(Products).filter(Products.type_id == type_id).order_by(
        desc(Products.Update_time)).all()
    return render_template('main/type_products.html', products=products, nav_types=get_nav_types(),
                           this_type=this_one_type)


