# coding:utf-8
# project/furniture/forms.py


from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, TextAreaField, IntegerField, SelectField, FileField,\
    SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy.sql import select
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import Tips, Types, Pictures, Products, ProductsTips


class TipEditForm(Form):
    tip_name = StringField(u'标签名称')
    tip_note = TextAreaField(u'标签描述')











