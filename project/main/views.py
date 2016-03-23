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

################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/')
def home():
    return render_template('main/index.html')
