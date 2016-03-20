# coding:utf-8
# project/furniture/views.py

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from project.models import Tips
from project import db
from .forms import TipEditForm

furniture_blueprint = Blueprint('furniture', __name__,)


@furniture_blueprint.route('/tip_create', methods=['GET', 'POST'])
def tip_create():
    form = TipEditForm(request.form)
    if form.validate_on_submit():
        tip = Tips(tip_name=form.tip_name.data, tip_note=form.tip_note.data)
        db.session.add(tip)
        db.session.commit()

        flash(u'创建成功', 'success')

        return redirect(url_for('furniture.tip_list'))

    return render_template('furniture/tip_edit.html', form=form)


@furniture_blueprint.route('/tip_edit/<tip_id>', methods=['GET', 'POST'])
def tip_edit(tip_id):
    # 先获取tip对象
    tip = db.session.query(Tips).get(tip_id)
    # 如果request.form空，使用tip对象
    form = TipEditForm(request.form, tip)
    if form.validate_on_submit():
        tip = Tips(tip_id=tip_id, tip_name=form.tip_name.data, tip_note=form.tip_note.data)
        db.session.merge(tip)
        db.session.commit()

        flash(u'更新成功', 'success')

        return redirect(url_for('furniture.tip_list'))

    return render_template('furniture/tip_edit.html', form=form)


@furniture_blueprint.route('/tip_delete/<tip_id>')
def tip_delete(tip_id):
    tip = db.session.query(Tips).get(tip_id)
    if tip:
        db.session.delete(tip)
        db.session.commit()

        flash(u'删除成功', 'success')

        return redirect(url_for('furniture.tip_list'))

    else:
        flash(u'数据不存在', 'danger')

        return redirect(url_for('furniture.tip_list'))


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


@furniture_blueprint.route('/tips/<page_id>')
@furniture_blueprint.route('/tips')
def tip_list(page_id=1):
    page_index = get_page_index(page_id)
    paginate = Tips.query.paginate(page_index, 5, False)
    num = db.session.query(Tips).filter().count()
    tips = paginate.items

    return render_template('furniture/tips.html', pagination=paginate, tips=tips)


