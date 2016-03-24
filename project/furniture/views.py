# coding:utf-8
# project/furniture/views.py

from flask import render_template, Blueprint, url_for, redirect, flash, request
from project.models import Tips, Types, Products, ProductsTips, Pictures
from project import db
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists
from .forms import TipEditForm, Form, StringField, TextAreaField, IntegerField, SelectField, FileField,\
    SelectMultipleField
from .apis import Page, up_to_qiniu
import uuid
import datetime
from flask.ext.login import login_required

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
@login_required
def tip_create():
    form = TipEditForm(request.form)
    if form.validate_on_submit():
        tip = Tips(tip_name=form.tip_name.data, tip_note=form.tip_note.data)
        db.session.add(tip)
        db.session.commit()
        flash(u'创建成功', 'success')
        return redirect(url_for('furniture.tip_list'))
    return render_template('furniture/tip_edit.html', form=form)


@furniture_blueprint.route('/tip_edit/<int:tip_id>', methods=['GET', 'POST'])
@login_required
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


@furniture_blueprint.route('/tip_delete/<int:tip_id>')
@login_required
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


@furniture_blueprint.route('/tips/<int:page_id>')
@furniture_blueprint.route('/tips')
@login_required
def tip_list(page_id=1):
    page_index = get_page_index(page_id)
    paginate = Tips.query.paginate(page_index, PAGE_SIZE, False)
    num = Tips.query.filter().count()
    page = Page(num, page_index, page_size=PAGE_SIZE)

    return render_template('furniture/tips.html', pagination=paginate, page=page)


# types


@furniture_blueprint.route('/types/<int:page_id>')
@furniture_blueprint.route('/types')
@login_required
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


def get_parent():
    parent_type_choices = [(0, u'无')]
    types = Types.query.filter().all()
    for this_type in types:
        parent_type_choices.append((this_type.type_id, this_type.type_name))
    return parent_type_choices


@furniture_blueprint.route('/type_edit/<int:type_id>', methods=['GET', 'POST'])
@furniture_blueprint.route('/type_create', methods=['GET', 'POST'])
@login_required
def type_edit(type_id=None):
    class TypesForm(Form):
        type_name = StringField(u'类型名称')
        type_note = TextAreaField(u'类型描述')
        parent_type_id = SelectField(u'上级类型', choices=get_parent())

    if type_id:
        this_type = db.session.query(Types).get(type_id)
    else:
        this_type = Types()
    form = TypesForm(request.form, this_type)
    if request.method == 'POST':
        this_type.type_name = form.type_name.data
        this_type.type_note = form.type_note.data
        this_type.parent_type_id = form.parent_type_id.data
        if type_id:
            db.session.merge(this_type)
            flash(u'更新成功', 'success')
        else:
            db.session.add(this_type)
            flash(u'新增成功', 'success')
        db.session.commit()
        return redirect(url_for('furniture.types_list'))
    return render_template('furniture/type_edit.html', form=form)


'''
@furniture_blueprint.route('/type_create2', methods=['GET', 'POST'])
@login_required
def type_create():
    class TypesForm(Form):
        type_name = StringField(u'类型名称')
        type_note = TextAreaField(u'类型描述')
        parent_type_id = SelectField(u'上级类型', choices=get_parent())

    form = TypesForm(request.form)
    if request.method == 'POST':
        this_type = Types(type_name=form.type_name.data, type_note=form.type_note.data,
                          parent_type_id=form.parent_type_id.data)
        db.session.add(this_type)
        db.session.commit()
        flash(u'新增成功', 'success')
        return redirect(url_for('furniture.types_list'))
    return render_template('furniture/type_edit.html', form=form)
'''


@furniture_blueprint.route('/type_delete/<int:type_id>')
@login_required
def type_delete(type_id):
    this_type = db.session.query(Types).get(type_id)
    if this_type:
        if db.session.query(Types).filter(exists().where(Types.parent_type_id == type_id)).count() > 0:
            flash(u'存在子类型，不可删除', 'danger')
            return redirect(url_for('furniture.types_list'))
        db.session.delete(this_type)
        db.session.commit()
        flash(u'删除成功', 'success')
        return redirect(url_for('furniture.types_list'))
    else:
        flash(u'数据不存在', 'danger')
        return redirect(url_for('furniture.types_list'))


def get_tips():
    tips_choices = [(0, u'无')]
    tips = Tips.query.filter().all()
    for tip in tips:
        tips_choices.append((tip.tip_id, tip.tip_name))
    return tips_choices


# 验证文件格式
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md', 'py'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@furniture_blueprint.route('/product_edit/<int:product_id>', methods=['GET', 'POST'])
@furniture_blueprint.route('/product_create', methods=['GET', 'POST'])
@login_required
def product_edit(product_id=None):

    class ProductForm(Form):
        type_id = SelectField(u'产品类型', choices=get_parent())
        product_code = StringField(u'产品编码')
        product_name = StringField(u'产品名称')
        product_text = TextAreaField(u'产品简介')
        product_md = TextAreaField(u'产品详情')
        is_on_first = SelectField(u'是否显示在首页', choices=[(0, u'否'), (1, u'是')])
        is_rolling = SelectField(u'是否首页滚动展示', choices=[(0, u'否'), (1, u'是')])
        main_picture = FileField(u'产品主图')
        product_tips = SelectMultipleField(u'产品标签', choices=get_tips())

    if product_id:
        product = db.session.query(Products).get(product_id)
    else:
        product = Products()

    form = ProductForm(request.form, product)
    if request.method == 'POST':
        product.product_code = form.product_code.data
        product.product_name = form.product_name.data
        product.product_text = form.product_text.data
        product.product_md = form.product_md.data
        product.type_id = form.type_id.data
        product.is_on_first = form.is_on_first.data
        product.is_rolling = form.is_rolling.data

        # product.product_tips = form.product_tips.data
        # 处理主图片及其url
        main_picture = request.files['main_picture']
        if main_picture and allowed_file(main_picture.filename):
            up_to_qiniu(product.main_picture, '', 0)
            product.main_picture = str(uuid.uuid1()) + '.' + main_picture.filename.rsplit('.', 1)[1]
            up_to_qiniu(product.main_picture, main_picture, 1)
            product.main_picture_url = 'http://7xrwf4.com1.z0.glb.clouddn.com/%s' % product.main_picture
        # 保存数据
        if product_id:
            product.Update_time = datetime.datetime.now()
            db.session.merge(product)
            flash(u'更新成功', 'success')
        else:
            product.create_time = datetime.datetime.now()
            product.Update_time = datetime.datetime.now()
            db.session.add(product)
            flash(u'新增成功', 'success')
        db.session.flush()
        # 获取主键
        product_id = product.product_id
        db.session.commit()

        # 处理标签
        old_tips = db.session.query(ProductsTips).filter(ProductsTips.product_id == product_id).all()
        for old_tip in old_tips:
            db.session.delete(old_tip)
            db.session.commit()

        for tip in form.product_tips.data:
            product_tip = ProductsTips(product_id=product_id,
                                       tip_id=tip)
            db.session.add(product_tip)
            db.session.commit()

        # 获取到其它图片
        product_pictures = request.files.getlist('product_pictures')

        # 如果重新上传了图片，删掉原来的图片，再插入新的图片
        for product_picture in product_pictures:
                if product_picture and allowed_file(product_picture.filename):
                    pictures = db.session.query(Pictures).filter(Pictures.product_id == product_id).all()
                    for picture in pictures:
                        up_to_qiniu(picture.picture_name, '', 0)
                        db.session.delete(picture)
                        db.session.commit()
                    break

        for product_picture in product_pictures:
            if product_picture and allowed_file(product_picture.filename):
                product_picture.filename = str(uuid.uuid1()) + '.' + product_picture.filename.rsplit('.', 1)[1]
                up_to_qiniu(product_picture.filename, product_picture, 1)
                picture = Pictures(picture_name=product_picture.filename,
                                   picture_url='http://7xrwf4.com1.z0.glb.clouddn.com/%s' % product_picture.filename,
                                   product_id=product_id)
                db.session.add(picture)
                db.session.commit()

        return redirect(url_for('furniture.products_list'))

    # 查询标签，并组成列表
    tips = db.session.query(ProductsTips).filter(ProductsTips.product_id == product_id).all()
    form.product_tips.data = []
    for tip in tips:
        form.product_tips.data.append(str(tip.tip_id))
    return render_template('furniture/product_edit.html', form=form)


@furniture_blueprint.route('/products')
@furniture_blueprint.route('/products/<int:page_id>')
@login_required
def products_list(page_id=1):
    page_index = get_page_index(page_id)
    # paginate = Products.query.paginate(page_index, PAGE_SIZE, False)
    num = Products.query.filter().count()
    page = Page(num, page_index, page_size=PAGE_SIZE)
    products = db.session.query(Products, Types)\
        .outerjoin(Types, Products.type_id == Types.type_id)\
        .filter().all()[page.offset:page.offset+page.limit]

    return render_template('furniture/products.html', products=products, page=page)


@furniture_blueprint.route('/product_delete/<int:product_id>')
@login_required
def product_delete(product_id):
    product = db.session.query(Products).get(product_id)

    if product:
        product_id = product.product_id
        up_to_qiniu(product.main_picture, '', 0)

        product_tips = db.session.query(ProductsTips).filter(ProductsTips.product_id == product_id).all()
        for product_tip in product_tips:
            db.session.delete(product_tip)
            db.session.commit()

        product_pictures = db.session.query(Pictures).filter(Pictures.product_id == product_id).all()
        for product_picture in product_pictures:
            up_to_qiniu(product_picture.picture_name, '', 0)
            db.session.delete(product_picture)
            db.session.commit()

        db.session.delete(product)
        db.session.commit()
        flash(u'删除成功', 'success')
        return redirect(url_for('furniture.products_list'))
    else:
        flash(u'产品不存在', 'danger')
        return redirect(url_for('furniture.products_list'))




