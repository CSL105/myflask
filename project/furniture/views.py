# coding:utf-8
# project/furniture/views.py

from flask import render_template, Blueprint, url_for, redirect, flash, request
from project.models import Tips, Types
from project import db
from sqlalchemy.orm import aliased
from .forms import TipEditForm, TypesForm
from .apis import Page

furniture_blueprint = Blueprint('furniture', __name__,)
PAGE_SIZE = 5


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


# tips


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


@furniture_blueprint.route('/tips/<page_id>')
@furniture_blueprint.route('/tips')
def tip_list(page_id=1):
    page_index = get_page_index(page_id)
    paginate = Tips.query.paginate(page_index, PAGE_SIZE, False)

    return render_template('furniture/tips.html', pagination=paginate)


# types


@furniture_blueprint.route('/types/<page_id>')
@furniture_blueprint.route('/types')
def types_list(page_id=1):
    # 转义 Types AS parent_types
    parent_types = aliased(Types, name='parent_types')
    page_index = get_page_index(page_id)
    # query = db.session.query(Types, parent_types).filter(Types.parent_type_id == parent_types.type_id)
    # query = query.outerjoin(parent_types, parent_types.parent_type_id == Types.type_id)
    num = Types.query.filter().count()
    page = Page(num, page_index, page_size=PAGE_SIZE)
    # 此次join查询，返回的types包含Types和parent_types，然后就可以获取到父类型的type_name了
    types = db.session.query(Types, parent_types)\
        .outerjoin(parent_types, parent_types.type_id == Types.parent_type_id)\
        .filter().all()[page.offset:page.offset+page.limit]

    return render_template('furniture/types.html', page=page, types=types)


@furniture_blueprint.route('/type_edit/<type_id>', methods=['GET', 'POST'])
def type_edit(type_id):
    type = db.session.query(Types).get(type_id)
    form = TypesForm(request.form, type)
    if form.validate_on_submit():
        type = Types(type_id=type_id, type_name=form.type_name.data,
                     type_note=form.type_note.data, parent_type_id=form.parent_type_id.data)
        db.session.merge(type)
        db.session.commit()
        flash(u'更新成功', 'success')
        return redirect(url_for('furniture.types_list'))
    return render_template('furniture/type_edit.html', form=form)



