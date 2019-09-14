from flask import render_template, redirect, url_for, request, jsonify, session
from app.test import bp
import braintree
from app.test.gateway import generate_client_token, transact, find_transaction
from flask_login import login_required


# Card number: 4111 1111 1111 1111
# Expiry: 09/20
# CVV: 400
# Postal Code: 40000


dummy_db = [
{'id':'0','title':'Flower','image':'flower.jpg','price':12.99},
{'id':'1','title':'Cat','image':'cat.jpg','price':24.00},
{'id':'2','title':'Ball','image':'ball.jpg','price':19.15}
]


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

def get_item(id):
    for d in dummy_db:
        if d['id'] == id:
            return d
    return None


def update_cart_qty(id,qty):
    for count, c in enumerate(session['cart']):
        if c['id'] == id:
            c['qty'] += 1
            session['cart'][count] = c
            session.modified = True
            return True
    return False


def get_data():
    data = []
    for c in session['cart']:
        item = get_item(c['id'])
        if item:
            item['qty'] = c['qty']
            data.append(item)
    return data


def get_total(data):
    total = 0
    for d in data:
        total = total + (d['qty'] * d['price'])
    return round(total,2)


def get_total_no_items(data):
    total_no_items = 0
    for d in data:
        total_no_items += d['qty']
    return total_no_items


@bp.route('/shop', methods=['GET'])
@login_required
def shop():
    return render_template('test/shop.html', data=dummy_db)


@bp.route('/cart', methods=['GET'])
@login_required
def cart():
    if 'cart' not in session:
        session['cart'] = []
    data = get_data()

    return render_template('test/cart.html', data=data, total=get_total(data), total_no_items=get_total_no_items(data))


# AJAX call to add item to cart
@bp.route('/cart/add', methods=['POST'])
@login_required
def add_cart():
    if 'cart' not in session:
        session['cart'] = []
    id = request.form['id']
    if not update_cart_qty(id,1):
        item = {
            'id' : id,
            'qty' : 1,
        }
        session['cart'].append(item)
        session.modified = True
    total_qty = 0
    for c in session['cart']:
        total_qty += c['qty']

    return jsonify({'count': total_qty})


@bp.route('/cart/remove/<id>', methods=['POST'])
@login_required
def remove_cart(id):
    # id in url is index of the session variable cart
    del session['cart'][int(id)]
    session.modified=True
    return redirect(url_for('test.cart'))


@bp.route('/cart/update/<id>', methods=['POST'])
@login_required
def update_cart(id):
    # id in url is index of the session variable cart
    item = session['cart'][int(id)]
    item['qty'] = int(request.form['qty'+id])
    session['cart'][int(id)] = item
    session.modified=True
    return redirect(url_for('test.cart'))


@bp.route('/clear_cart', methods=['GET'])
@login_required
def clear_cart():
    session.pop('cart', None)
    return ('', 204)


@bp.route('/checkout', methods=['GET'])
@login_required
def checkout():
    client_token = generate_client_token()
    data = get_data()
    return render_template('test/checkout.html', client_token=client_token, data=data, total=get_total(data), total_no_items=get_total_no_items(data))


@bp.route('/checkout/result/<transaction_id>', methods=['GET'])
@login_required
def result_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }
    return render_template('test/result_checkout.html', transaction=transaction, result=result)


@bp.route('/checkout/create', methods=['POST'])
@login_required
def create_checkout():
    result = transact({
        'amount': request.form['total_amt'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('test.result_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors:
            flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('test.checkout'))
