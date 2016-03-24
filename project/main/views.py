# project/main/views.py


#################
#### imports ####
#################

from flask.ext.login import login_required
from flask import render_template, Blueprint, url_for, redirect, flash, request
from project.models import Tips, Types, Products, ProductsTips, Pictures
from project import db
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists
from sqlalchemy import desc

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
    main_picture_urls = []
    main_picture_products = db.session.query(Products).filter(Products.is_rolling == 1).order_by(desc(Products.Update_time)).limit(5).offset(0)
    for main_product in main_picture_products:
        main_picture_urls.append((main_product.main_picture_url, main_product.product_id))
    rolling_num = len(main_picture_urls)
    return render_template('main/index.html', main_picture_urls=main_picture_urls, rolling_num=rolling_num)




