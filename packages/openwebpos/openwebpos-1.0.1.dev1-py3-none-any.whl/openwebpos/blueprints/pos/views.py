from escpos import *

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from openwebpos.blueprints.billing.models import PaymentMethod, Payment, Invoice
from openwebpos.blueprints.billing.forms import PaymentAmountForm

from .models import MenuType, MenuCategory, MenuItem, OrderType, Order, \
    OrderItem
from .forms import QuantityForm

pos = Blueprint('pos', __name__, template_folder='templates', url_prefix='/pos')


@pos.before_request
@login_required
def before_request():
    """
    Protects all the pos endpoints.
    """
    pass


def test_printer():
    receipt_printer = printer.Network("172.20.40.7")
    return receipt_printer


def kitchen_receipt(invoice_id):
    """
    Prints a kitchen receipt for the given invoice id.
    """

    # price = 0
    # quantity = 0
    # item_option = ''
    purchases = []
    receipt_width = 24

    invoice = Invoice.query.get(invoice_id)
    order_items = OrderItem.query.filter_by(order_id=invoice.order_id).all()

    receipt_content = [
        'Kitchen'.center(receipt_width),
    ]

    for item in order_items:
        item_category = item.menu_item.menu_category.name
        item_name = item.menu_item.name
        item_quantity = item.quantity
        purchases.append((item_category, item_name, item_quantity))

    for item_category, item_name, item_quantity in purchases:
        line_item = str(item_quantity) + ' ' + item_category + ' ' + item_name
        purchase_line = line_item.ljust(receipt_width)
        receipt_content.append(purchase_line)

    receipt_printer = printer.Network("172.20.40.7")
    receipt_printer.set(height=3, width=3, font='b', text_type='B')
    receipt_printer.text("\n".join(receipt_content))
    receipt_printer.cut()


def customer_receipt(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    _invoice_due = invoice.due
    if _invoice_due <= 0:
        _invoice_due = 0
    _payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    _company_name = 'Company Name'
    _company_address = '1234 Some-Address St.'
    _company_city = 'City'
    _company_state = 'TX'
    _company_zip = '12345'
    _order_date = Invoice.query.filter_by(
        id=invoice_id).first_or_404().created_at

    price = 0
    quantity = 0
    receipt_subtotal = 0
    purchases = []
    receipt_width = 48

    # shop_name = _store.name.title().center(receipt_width)
    shop_name = _company_name.title().center(receipt_width)
    shop_address = f'{_company_address}\n{_company_city}, {_company_state} {_company_zip}'
    shop_address = shop_address.splitlines()
    order_date = f'{_order_date.strftime("%m/%d/%Y %I:%M %p")}'
    receipt_message = 'Thank you for your business!\nPlease come again!'
    receipt_message = receipt_message.splitlines()
    # receipt_subtotal += price * quantity
    tax_percentage = 8.25
    tax_percentage = "{:.0%}".format(tax_percentage)
    # receipt_total = 0
    receipt_content = [
        shop_name,
        shop_address[0].center(receipt_width),
        shop_address[1].center(receipt_width),
        '\n',
    ]

    # order_id = Order.query.filter_by(orderNumber=order_number).first_or_404().id
    order_items = OrderItem.query.filter_by(order_id=invoice.order_id).all()
    for order_item in order_items:
        name = order_item.menu_item.menu_category.name + ' - ' + order_item.menu_item.name
        quantity = order_item.quantity
        price = order_item.menu_item.price
        receipt_subtotal += price * quantity
        purchases.append((name, quantity, price), )

    for name, quantity, price in purchases:
        line_subtotal = '$' + str(round(quantity * price, 2))
        purchase_line = f'{name}'.ljust(receipt_width - len(line_subtotal), '.')
        purchase_line += line_subtotal
        if type(quantity) is int and quantity >= 1:
            purchase_line += f'     {quantity} @ {price} /ea'
        receipt_content.append(purchase_line)

    receipt_subtotal = str(round(receipt_subtotal, 2))
    receipt_tax = str(round(float(receipt_subtotal) * 0.0825, 2))
    receipt_total = str(round(float(receipt_subtotal) + float(receipt_tax), 2))

    receipt_content.append('\n')
    receipt_content.append('    Subtotal: '.rjust(
        receipt_width - len(receipt_subtotal) - 1) + '$' + receipt_subtotal)
    receipt_content.append('    Tax: '.rjust(
        receipt_width - len(receipt_tax) - 1) + '$' + receipt_tax)
    receipt_content.append('    Total: '.rjust(
        receipt_width - len(receipt_total) - 1) + '$' + receipt_total)
    payment = _payments[-1]
    receipt_content.append('    Payment Method: '.rjust(
        receipt_width - len(
            receipt_total) - 2) + payment.payment_method.name)
    receipt_content.append('    Payment Amount: '.rjust(
        receipt_width - len(receipt_total) - 2) + '$' + str(payment.amount))
    receipt_content.append('    Change: '.rjust(
        receipt_width - len(receipt_total) - 2) + '$' + str(payment.change))
    receipt_content.append('    Due: '.rjust(
        receipt_width - len(receipt_total) - 2) + '$' + str(_invoice_due))

    receipt_content.append('\n'.ljust(receipt_width, '*'))
    receipt_content.append(receipt_message[0].center(receipt_width))
    receipt_content.append(receipt_message[1].center(receipt_width))
    receipt_content.append(f'{order_date}'.center(receipt_width))

    receipt_printer = test_printer()
    receipt_printer.set(height=1, width=1)
    receipt_printer.text("\n".join(receipt_content))
    receipt_printer.cut()


@pos.get('/print/<int:invoice_id>/<string:receipt_type>')
def print_receipt(invoice_id, receipt_type):
    """
    Prints a test receipt.
    """
    if receipt_type == 'kitchen':
        kitchen_receipt(invoice_id)
    elif receipt_type == 'customer':
        customer_receipt(invoice_id)
    return redirect(url_for('pos.index'))


@pos.route('/')
def index():
    active_order_types = OrderType.query.filter_by(active=True).all()
    active_orders = Order.query.filter_by(active=True).all()
    if active_orders:
        return render_template('pos/active_orders.html', title='Active Orders',
                               active_orders=active_orders,
                               order_types=active_order_types)
    return render_template('pos/index.html', title='POS',
                           order_types=active_order_types)


@pos.route('/create/<int:order_type_id>')
def create_order(order_type_id):
    order_type = OrderType.query.get(order_type_id)
    _order = Order(order_type=order_type)
    _order.save()
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.route('/order/<int:order_id>')
def order(order_id):
    _order = Order.query.get(order_id)
    _menu_types = MenuType.query.filter_by(active=True).all()
    _order_items = OrderItem.query.filter_by(order_id=_order.id).all()
    form = QuantityForm()
    return render_template('pos/order.html', title='Order', order=_order,
                           menu_types=_menu_types, order_items=_order_items,
                           form=form)


@pos.get('/order/<int:order_id>/toggle')
def toggle_order(order_id):
    _order = Order.query.get(order_id)
    _order.toggle()
    return redirect(url_for('pos.index'))


@pos.route('/order/<int:order_id>/<int:menu_type_id>')
def order_menu_type(order_id, menu_type_id):
    _order = Order.query.get(order_id)
    _menu_type = MenuType.query.get(menu_type_id)
    _menu_categories = MenuCategory.query.filter_by(
        menu_type_id=menu_type_id, active=True).all()
    return render_template('pos/order_menu_type.html', title='Order',
                           order=_order, menu_type=_menu_type,
                           menu_categories=_menu_categories)


@pos.route('/order/<int:order_id>/<int:menu_type_id>/<int:menu_category_id>')
def order_menu_category(order_id, menu_type_id, menu_category_id):
    _order = Order.query.get(order_id)
    _menu_type = MenuType.query.get(menu_type_id)
    _menu_category = MenuCategory.query.get(menu_category_id)
    _menu_items = MenuItem.query.filter_by(
        menu_category_id=menu_category_id, active=True).all()
    form = QuantityForm()
    return render_template('pos/order_menu_category.html', title='Order',
                           order=_order, menu_type=_menu_type,
                           menu_category=_menu_category, menu_items=_menu_items,
                           form=form)


@pos.post('/order/add_item/<int:order_id>/<int:menu_item_id>')
def order_add_item(order_id, menu_item_id):
    _order = Order.query.get(order_id)
    _menu_item = MenuItem.query.get(menu_item_id)
    form = QuantityForm()
    if form.validate_on_submit():
        _order_item = OrderItem(order_id=order_id, menu_item_id=_menu_item.id,
                                quantity=form.quantity.data)
        _order_item.save()
        _order.update_totals()
    return redirect(url_for('pos.order', order_id=_order.id))


@pos.get('/invoice/order/<int:order_id>')
def invoice_order(order_id):
    _order = Order.query.get(order_id)
    if _order.is_invoiced():
        return redirect(url_for('.invoice', invoice_id=_order.invoice.id))
    _invoice = Invoice(order_id=_order.id, tax=_order.tax_total,
                       subtotal=_order.subtotal, total=_order.total,
                       due=_order.total)
    _invoice.save()
    _order.set_invoiced()
    kitchen_receipt(_invoice.id)
    return redirect(url_for('.invoice', invoice_id=_invoice.id))


@pos.route('/invoice/<int:invoice_id>')
def invoice(invoice_id):
    _invoice = Invoice.query.get(invoice_id)
    _payment_methods = PaymentMethod.query.filter_by(active=True).all()
    _payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    form = PaymentAmountForm()
    return render_template('pos/invoice.html', title='Invoice', form=form,
                           invoice=_invoice, payment_methods=_payment_methods,
                           payments=_payments)


@pos.post('/payment/<int:invoice_id>')
def payment(invoice_id):
    _invoice = Invoice.query.get(invoice_id)
    form = PaymentAmountForm()
    payment_method_id = request.form.get('payment_method_id')
    if form.validate_on_submit():
        _payment = Payment(invoice_id=invoice_id, amount=form.amount.data,
                           payment_method_id=payment_method_id)
        _payment.save()
        _payment.update_invoice_due()
    return redirect(url_for('pos.invoice', invoice_id=invoice_id))


@pos.post('/order/pay/<int:order_id>/<int:payment_method_id>')
def order_pay_method(order_id, payment_method_id):
    _order = Order.query.get(order_id)
    _payment_method = PaymentMethod.query.get(payment_method_id)
    form = PaymentAmountForm()
    if form.validate_on_submit():
        _payment = Payment(invoice_id=order_id,
                           payment_method_id=_payment_method.id,
                           amount=form.amount.data)
        _payment.save()
        _order.update_totals()
        if _payment.amount >= _order.total:
            _order.set_paid()
            order_total = _order.subtotal + _order.tax_total
            _invoice = Invoice(order_id=_order.id, tax=_order.tax_total,
                               subtotal=_order.subtotal, total=order_total)
            _invoice.save()
            return redirect(url_for('pos.order', order_id=_order.id))
    return redirect(url_for('pos.order', order_id=_order.id))
