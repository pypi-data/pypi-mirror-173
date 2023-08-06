from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from openwebpos.blueprints.pos.models import MenuType, MenuCategory, MenuItem
from openwebpos.blueprints.pos.forms import MenuTypeForm, MenuCategoryForm, \
    MenuItemForm, IngredientForm, MenuItemIngredientForm

from openwebpos.blueprints.pos.models import OrderType, Order, Ingredient, \
    MenuItemIngredient
from openwebpos.blueprints.user.models import User
from openwebpos.blueprints.billing.models import PaymentMethod, Payment, Invoice

admin = Blueprint('admin', __name__, template_folder='templates',
                  url_prefix='/admin')


@admin.before_request
@login_required
def before_request():
    """
    Protects all the admin endpoints.
    """
    pass


@admin.route('/')
def index():
    return render_template('admin/index.html', title='Admin')


@admin.route('/users')
def users():
    _users = User.query.all()
    return render_template('admin/users.html', title='Users', users=_users)


@admin.route('/menus')
def menus():
    return render_template('admin/menus.html', title='Menus')


@admin.route('/menu/types')
def menu_types():
    _menu_types = MenuType.query.all()
    return render_template('admin/menu_types.html', title='Menu Types',
                           menu_types=_menu_types)


@admin.route('/menu/types/toggle/<int:menu_type_id>')
def toggle_menu_type(menu_type_id):
    _menu_type = MenuType.query.get(menu_type_id)
    _menu_type.toggle()
    return redirect(url_for('admin.menu_types'))


@admin.route('/menu/types/edit/<int:menu_type_id>', methods=['GET', 'POST'])
def edit_menu_type(menu_type_id):
    _menu_type = MenuType.query.get(menu_type_id)
    form = MenuTypeForm(obj=_menu_type)
    if form.validate_on_submit():
        form.populate_obj(_menu_type)
        _menu_type.update()
        return redirect(url_for('admin.menu_types'))
    return render_template('admin/edit_menu_type.html', title='Edit Menu Type',
                           menu_type=_menu_type, form=form)


@admin.route('/menu/types/delete/<int:menu_type_id>')
def delete_menu_type(menu_type_id):
    _menu_type = MenuType.query.get(menu_type_id)
    _menu_type.delete()
    return redirect(url_for('admin.menu_types'))


@admin.route('/menu/categories', methods=['GET', 'POST'])
def menu_categories():
    _menu_categories = MenuCategory.query.all()
    form = MenuCategoryForm()
    form.set_choices()
    if form.validate_on_submit():
        _menu_category = MenuCategory()
        form.populate_obj(_menu_category)
        _menu_category.save()
        return redirect(url_for('admin.menu_categories'))
    return render_template('admin/menu_categories.html',
                           title='Menu Categories',
                           menu_categories=_menu_categories, form=form)


@admin.get('/menu/categories/toggle/<int:menu_category_id>')
def toggle_menu_category(menu_category_id):
    _menu_category = MenuCategory.query.get(menu_category_id)
    _menu_category.toggle()
    return redirect(url_for('admin.menu_categories'))


@admin.route('/menu/categories/edit/<int:menu_category_id>',
             methods=['GET', 'POST'])
def edit_menu_category(menu_category_id):
    _menu_category = MenuCategory.query.get(menu_category_id)
    form = MenuCategoryForm(obj=_menu_category)
    form.set_choices()
    if form.validate_on_submit():
        form.populate_obj(_menu_category)
        _menu_category.update()
        return redirect(url_for('admin.menu_categories'))
    return render_template('admin/edit_menu_category.html',
                           title='Edit Menu Category',
                           menu_category=_menu_category, form=form)


@admin.get('/menu/categories/delete/<int:menu_category_id>')
def delete_menu_category(menu_category_id):
    _menu_category = MenuCategory.query.get(menu_category_id)
    _menu_category.delete()
    return redirect(url_for('admin.menu_categories'))


@admin.route('/menu/items', methods=['GET', 'POST'])
def menu_items():
    _menu_items = MenuItem.query.all()
    form = MenuItemForm()
    form.set_choices()
    if form.validate_on_submit():
        _menu_item = MenuItem()
        form.populate_obj(_menu_item)
        _menu_item.save()
        return redirect(url_for('admin.menu_items'))
    return render_template('admin/menu_items.html', title='Menu Items',
                           menu_items=_menu_items, form=form)


@admin.get('/menu/items/toggle/<int:menu_item_id>')
def toggle_menu_item(menu_item_id):
    _menu_item = MenuItem.query.get(menu_item_id)
    _menu_item.toggle()
    return redirect(url_for('admin.menu_items'))


@admin.route('/menu/items/edit/<int:menu_item_id>', methods=['GET', 'POST'])
def edit_menu_item(menu_item_id):
    _menu_item = MenuItem.query.get(menu_item_id)
    form = MenuItemForm(obj=_menu_item)
    form.set_choices()
    if form.validate_on_submit():
        form.populate_obj(_menu_item)
        _menu_item.update()
        return redirect(url_for('admin.menu_items'))
    return render_template('admin/edit_menu_item.html', title='Edit Menu Item',
                           menu_item=_menu_item, form=form)


@admin.get('/menu/items/delete/<int:menu_item_id>')
def delete_menu_item(menu_item_id):
    _menu_item = MenuItem.query.get(menu_item_id)
    _menu_item.delete()
    return redirect(url_for('admin.menu_items'))


@admin.route('/menu/ingredients/<int:menu_item_id>', methods=['GET', 'POST'])
def menu_item_ingredients(menu_item_id):
    _menu_item_ingredients = MenuItemIngredient.query.filter_by(
        menu_item_id=menu_item_id).all()
    _menu_item = MenuItem.query.get(menu_item_id)
    form = MenuItemIngredientForm()
    form.set_choices()
    if form.validate_on_submit():
        _item_ingredient = MenuItemIngredient(menu_item_id=menu_item_id)
        form.populate_obj(_item_ingredient)
        _item_ingredient.save()
        return redirect(
            url_for('admin.menu_item_ingredients', menu_item_id=menu_item_id))
    return render_template('admin/menu_item_ingredients.html',
                           title='Menu Item Ingredients', form=form,
                           menu_item_ingredients=_menu_item_ingredients,
                           menu_item=_menu_item)


@admin.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    _ingredients = Ingredient.query.all()
    form = IngredientForm()
    if form.validate_on_submit():
        _ingredient = Ingredient()
        form.populate_obj(_ingredient)
        _ingredient.save()
        return redirect(url_for('admin.ingredients'))
    return render_template('admin/ingredients.html', title='Ingredients',
                           form=form, ingredients=_ingredients)


@admin.get('/ingredients/toggle/<int:ingredient_id>')
def toggle_ingredient(ingredient_id):
    _ingredient = Ingredient.query.get(ingredient_id)
    _ingredient.toggle()
    return redirect(url_for('admin.ingredients'))


@admin.route('/orders')
def orders():
    _orders = Order.query.all()
    return render_template('admin/orders.html', title='Orders', orders=_orders)


@admin.route('/orders/types')
def order_types():
    _order_types = OrderType.query.all()
    return render_template('admin/order_types.html', title='Order Types',
                           order_types=_order_types)


@admin.route('/orders/types/toggle/<int:order_type_id>')
def toggle_order_type(order_type_id):
    _order_type = OrderType.query.get(order_type_id)
    _order_type.toggle()
    return redirect(url_for('admin.order_types'))


@admin.route('/billing')
def billing():
    return render_template('admin/billing.html', title='Billing')


@admin.route('/billing/payment_methods')
def payment_methods():
    _payment_methods = PaymentMethod.query.all()
    return render_template('admin/payment_methods.html',
                           title='Payment Methods',
                           payment_methods=_payment_methods)
