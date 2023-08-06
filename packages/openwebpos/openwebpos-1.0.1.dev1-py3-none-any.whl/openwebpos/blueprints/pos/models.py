from decimal import Decimal

from openwebpos.extensions import db
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin
from openwebpos.utils import gen_order_number


class Ingredient(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'ingredients'

    name = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    menu_item_ingredients = db.relationship('MenuItemIngredient',
                                            backref='ingredient',
                                            lazy='dynamic')
    active = db.Column(db.Boolean, default=True, nullable=False)

    def toggle(self):
        self.active = not self.active
        self.save()

    def __init__(self, **kwargs):
        super(Ingredient, self).__init__(**kwargs)


class MenuType(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'menu_types'

    short_name = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    menu_categories = db.relationship('MenuCategory', backref='menu_type',
                                      lazy='dynamic')

    def toggle(self):
        self.active = not self.active
        return self.update()

    @staticmethod
    def insert_default_menu_types():
        menu_types = [
            {'short_name': 'food', 'name': 'Food', 'description': 'Food'},
            {'short_name': 'drink', 'name': 'Drink', 'description': 'Drink'},
            {'short_name': 'alcohol', 'name': 'Alcohol',
             'description': 'Alcohol'},
            {'short_name': 'dessert', 'name': 'Dessert',
             'description': 'Dessert'},
            {'short_name': 'other', 'name': 'Other', 'description': 'Other'},
        ]

        for menu_type in menu_types:
            menu_type = MenuType(**menu_type)
            menu_type.save()

    def __init__(self, **kwargs):
        super(MenuType, self).__init__(**kwargs)


class MenuCategory(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'menu_categories'

    short_name = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    menu_type_id = db.Column(db.Integer, db.ForeignKey('menu_types.id'),
                             nullable=False)
    menu_items = db.relationship('MenuItem', backref='menu_category',
                                 lazy='dynamic')

    @staticmethod
    def insert_default_menu_categories():
        menu_categories = [
            {'short_name': 'pizza', 'name': 'Pizza', 'description': 'Pizza',
             'menu_type_id': 1},
        ]

        for menu_category in menu_categories:
            menu_category = MenuCategory(**menu_category)
            menu_category.save()

    def toggle(self):
        self.active = not self.active
        return self.update()

    @staticmethod
    def create(**kwargs):
        menu_category = MenuCategory(**kwargs)
        return menu_category.save()

    def __init__(self, **kwargs):
        super(MenuCategory, self).__init__(**kwargs)


class MenuItem(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'menu_items'
    short_name = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    menu_category_id = db.Column(db.Integer,
                                 db.ForeignKey('menu_categories.id'),
                                 nullable=False)
    order_items = db.relationship('OrderItem', backref='menu_item',
                                  lazy='dynamic')
    menu_item_ingredients = db.relationship('MenuItemIngredient',
                                            backref='menu_item', lazy='dynamic')

    @staticmethod
    def insert_default_menu_items():
        menu_items = [
            {'short_name': 'pepperoni', 'name': 'Pepperoni',
             'description': 'Pepperoni', 'price': Decimal('10.00'),
             'menu_category_id': 1},
        ]

        for menu_item in menu_items:
            menu_item = MenuItem(**menu_item)
            menu_item.save()

    def toggle(self):
        self.active = not self.active
        return self.update()

    def __init__(self, **kwargs):
        super(MenuItem, self).__init__(**kwargs)


class MenuItemIngredient(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'menu_item_ingredients'

    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'),
                             nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'),
                              nullable=False)
    quantity = db.Column(db.Numeric(8, 2), nullable=False)

    def __init__(self, **kwargs):
        super(MenuItemIngredient, self).__init__(**kwargs)


class OrderType(db.Model, CRUDMixin):
    __tablename__ = 'order_types'
    name = db.Column(db.String(255), nullable=False, unique=True)
    deletable = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)
    orders = db.relationship('Order', backref='order_type', lazy='dynamic')

    def toggle(self):
        self.active = not self.active
        return self.update()

    @staticmethod
    def insert_default_order_types():
        order_types = [
            {'name': 'Takeout', 'deletable': False},
            {'name': 'Dine In', 'deletable': False},
            {'name': 'Delivery', 'deletable': False},
            {'name': 'Drive Thru', 'deletable': False},
        ]

        for order_type in order_types:
            order_type = OrderType(**order_type)
            order_type.save()

    def __init__(self, **kwargs):
        super(OrderType, self).__init__(**kwargs)


class Order(db.Model, CRUDMixin):
    __tablename__ = 'orders'
    order_number = db.Column(db.String(255), nullable=False, unique=True)
    order_type_id = db.Column(db.Integer, db.ForeignKey('order_types.id'))
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic')
    tax_rate = db.Column(db.Numeric(8, 2), nullable=False,
                         default=Decimal(8.25))
    tax_total = db.Column(db.Numeric(8, 2), nullable=False,
                          default=Decimal(0.00))
    subtotal = db.Column(db.Numeric(8, 2), nullable=False,
                         default=Decimal(0.00))
    total = db.Column(db.Numeric(8, 2), nullable=False, default=Decimal(0.00))
    invoice = db.relationship('Invoice', backref='order', uselist=False)
    invoiced = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, default=True)

    # def is_paid(self):
    #     return self.payment_status == 'paid'
    #
    # def set_paid(self):
    #     self.payment_status = 'paid'
    #     return self.update()

    def is_invoiced(self):
        """Return True if the order has been invoiced."""
        return self.invoiced

    def not_invoiced(self):
        """Return True if the order has not been invoiced."""
        return not self.invoiced

    def set_invoiced(self):
        self.invoiced = True
        return self.update()

    def toggle(self):
        self.active = not self.active
        return self.update()

    def order_subtotal(self):
        return sum([order_item.total for order_item in self.order_items])

    def order_tax_total(self):
        return Decimal(self.order_subtotal() * self.tax_rate / 100)

    def order_total(self):
        return Decimal(self.order_subtotal() + self.order_tax_total())

    def update_totals(self):
        self.tax_total = self.order_tax_total()
        self.subtotal = self.order_subtotal()
        self.total = self.order_total()
        return self.update()

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.order_number = gen_order_number()
        self.total = self.order_total()


class OrderItem(db.Model, CRUDMixin):
    __tablename__ = 'order_items'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    quantity = db.Column(db.Integer, default=1)
    total = db.Column(db.Numeric(8, 2), default=Decimal(0.00))
    active = db.Column(db.Boolean, default=True)

    def order_item_total(self):
        menu_item = MenuItem.query.get(self.menu_item_id)
        return self.quantity * menu_item.price

    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)

        self.total = self.order_item_total()

# class Menu(DateTimeMixin, CRUDMixin, db.Model):
#     __tablename__ = 'menu'
#     name = db.Column(db.String(255), nullable=False)
#     active = db.Column(db.Boolean, default=True, nullable=False)
#     menu_items = db.relationship('Item', backref='menu', lazy='dynamic')
#     recepies = db.relationship('Recipe', backref='menu', lazy='dynamic')
#
#     def not_empty(self):
#         return self.menu_items.count() > 0
#
#     @staticmethod
#     def list_active():
#         return Menu.query.filter_by(active=True).all()
#
#     @staticmethod
#     def insert_menus(name):
#         """
#         Inserts a menu into the database.
#         """
#         menus = [
#             {'name': f'{name}'},
#         ]
#
#         for menu in menus:
#             menu = Menu(**menu)
#             menu.save()
#
#     def __init__(self, **kwargs):
#         super(Menu, self).__init__(**kwargs)


# class Ingredient(DateTimeMixin, CRUDMixin, db.Model):
#     __tablename__ = 'ingredients'
#
#     name = db.Column(db.String(60))
#     # recipes = db.relationship('Recipe', backref='ingredient', lazy='dynamic')
#     price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
#     addon = db.Column(db.Boolean, default=False)
#     order_item_options = db.relationship('OrderItemOption',
#                                          backref='ingredient', lazy='dynamic')
#     active = db.Column(db.Boolean, default=True)
#
#     @staticmethod
#     def insert_ingredients(name):
#         ingredients = [
#             {'name': f'{name}'},
#         ]
#
#         for ingredient in ingredients:
#             ingredient = Ingredient(**ingredient)
#             ingredient.save()
#
#     def not_in_menu(self, menu_id):
#         return not self.in_menu(menu_id)
#
#     # def in_menu(self, menu_id):
#     #     return Recipe.query.filter_by(ingredient_id=self.id,
#     #                                   menu_id=menu_id).first()
#
#     @staticmethod
#     def list_ingredients_not_in_menu(menu_id):
#         ingredients = Ingredient.query.filter_by(active=True).filter(
#             ~Ingredient.recipes.any(menu_id=menu_id)).all()
#         if ingredients:
#             return ingredients
#         return Ingredient.query.filter_by(active=True).all()
#
#     def __init__(self, **kwargs):
#         super(Ingredient, self).__init__(**kwargs)


# class Item(DateTimeMixin, CRUDMixin, db.Model):
#     __tablename__ = 'item'
#     name = db.Column(db.String(255), nullable=False)
#     price = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
#     active = db.Column(db.Boolean, default=True, nullable=False)
#     menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
#     order_items = db.relationship('OrderItem', backref='item',
#                                   lazy='dynamic')
#
#     @staticmethod
#     def insert_items(name, price, menu_id):
#         items = [
#             {'name': f'{name}', 'price': {price}, 'menu_id': {menu_id}},
#         ]
#
#         for item in items:
#             item = Item(**item)
#             item.save()
#
#     def __init__(self, **kwargs):
#         super(Item, self).__init__(**kwargs)


# class Recipe(CRUDMixin, db.Model):
#     __tablename__ = 'recipe'
#     menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'),
#                         nullable=False)
#     ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'),
#                               nullable=False)
#     quantity = db.Column(db.Integer, default=1, nullable=False)
#
#     def __init__(self, **kwargs):
#         super(Recipe, self).__init__(**kwargs)
