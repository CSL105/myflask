# coding:utf-8
# project/user/forms.py


from flask_wtf import Form
from wtforms import TextField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])


class RegisterForm(Form):
    email = StringField(
        u'邮箱',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    password = PasswordField(
        u'密码',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        u'再次输入密码',
        validators=[
            DataRequired(),
            EqualTo('password', message=u'密码不匹配')
        ]
    )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(u"邮箱已被注册")
            return False
        return True


class ChangePasswordForm(Form):
    password = PasswordField(
        u'新密码',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        u'再次输入密码',
        validators=[
            DataRequired(),
            EqualTo('password', message=u'密码必须匹配')
        ]
    )
