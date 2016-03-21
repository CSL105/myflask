# coding:utf-8
# project/furniture/forms.py


from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import Tips, Types, Pictures, Products, ProductsTips


class TipEditForm(Form):
    tip_name = StringField(u'标签名称')
    tip_note = TextAreaField(u'标签描述')


class TypesForm(Form):
    type_name = StringField(u'类型')
    type_note = TextAreaField(u'类型描述')
    parent_type_id = IntegerField(u'上级类型')

