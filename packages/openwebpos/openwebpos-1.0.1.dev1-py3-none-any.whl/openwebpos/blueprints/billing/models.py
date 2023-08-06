from openwebpos.extensions import db
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin
from openwebpos.utils import gen_order_number

from openwebpos.blueprints.pos.models import MenuItem
from openwebpos.blueprints.pos.models import Order


# class OrderType(db.Model, CRUDMixin):
#     __tablename__ = 'order_types'
#     name = db.Column(db.String(255), nullable=False, unique=True)
#     deletable = db.Column(db.Boolean, default=True)
#     active = db.Column(db.Boolean, default=True)
#     orders = db.relationship('Order', backref='order_type', lazy='dynamic')
#
#     def toggle(self):
#         self.active = not self.active
#         return self.update()
#
#     @staticmethod
#     def insert_default_order_types():
#         order_types = [
#             {'name': 'Takeout', 'deletable': False},
#             {'name': 'Dine In', 'deletable': False},
#             {'name': 'Delivery', 'deletable': False},
#             {'name': 'Drive Thru', 'deletable': False},
#         ]
#
#         for order_type in order_types:
#             order_type = OrderType(**order_type)
#             order_type.save()
#
#     def __init__(self, **kwargs):
#         super(OrderType, self).__init__(**kwargs)
#
#
# class Order(db.Model, CRUDMixin):
#     __tablename__ = 'orders'
#     order_number = db.Column(db.String(255), nullable=False, unique=True)
#     order_type_id = db.Column(db.Integer, db.ForeignKey('order_types.id'))
#     order_items = db.relationship('OrderItem', backref='order', lazy='dynamic')
#     active = db.Column(db.Boolean, default=True)
#
#     def __init__(self, **kwargs):
#         super(Order, self).__init__(**kwargs)
#         self.order_number = gen_order_number()
#
#
# class OrderItem(db.Model, CRUDMixin):
#     __tablename__ = 'order_items'
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
#     menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
#     quantity = db.Column(db.Integer, default=1)
#     total = db.Column(db.Float, default=0.0)
#     active = db.Column(db.Boolean, default=True)
#
#     def __init__(self, **kwargs):
#         super(OrderItem, self).__init__(**kwargs)
#
#         menu_item = MenuItem.query.get(self.menu_item_id)
#
#         self.total = menu_item.price * self.quantity


class PaymentMethod(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'payment_methods'
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    payments = db.relationship('Payment', backref='payment_method',
                               lazy='dynamic')

    @staticmethod
    def insert_default_payment_methods():
        payment_methods = [
            {'name': 'Cash', 'description': 'Cash payment'},
            {'name': 'Credit Card', 'description': 'Credit card payment'},
            {'name': 'Check', 'description': 'Check payment'},
            {'name': 'Gift Card', 'description': 'Gift card payment'},
        ]

        for payment_method in payment_methods:
            payment_method = PaymentMethod(**payment_method)
            payment_method.save()

    def __init__(self, **kwargs):
        super(PaymentMethod, self).__init__(**kwargs)


class Payment(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'payments'
    payment_method_id = db.Column(db.Integer,
                                  db.ForeignKey('payment_methods.id'),
                                  nullable=False)
    amount = db.Column(db.Numeric(8, 2), nullable=False)
    change = db.Column(db.Numeric(8, 2), nullable=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'),
                           nullable=False)

    def update_invoice_due(self):
        invoice = Invoice.query.get(self.invoice_id)
        invoice.due = invoice.due - self.amount
        invoice.update_payment_status()
        invoice.update()

    def __init__(self, **kwargs):
        super(Payment, self).__init__(**kwargs)
        invoice_total = Invoice.query.get(self.invoice_id).total

        change = self.amount - invoice_total
        if change > 0:
            self.change = change
        else:
            self.change = 0.0


class Invoice(db.Model, DateTimeMixin, CRUDMixin):
    __tablename__ = 'invoices'

    receipt_number = db.Column(db.String(100), nullable=False, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    tax = db.Column(db.Numeric(8, 2), nullable=False)
    subtotal = db.Column(db.Numeric(8, 2), nullable=False)
    total = db.Column(db.Numeric(8, 2), nullable=False)
    due = db.Column(db.Numeric(8, 2), nullable=False)
    payment_status = db.Column(db.String(100), nullable=False, default='unpaid')
    payments = db.relationship('Payment', backref='invoice', lazy='dynamic')

    def update_due(self):
        self.due = self.total - sum([p.amount for p in self.payments])
        self.update_payment_status()

    def update_payment_status(self):
        if self.due <= 0:
            self.payment_status = 'paid'
        elif self.due < self.total:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'

    def __init__(self, **kwargs):
        super(Invoice, self).__init__(**kwargs)
        self.receipt_number = gen_order_number()
