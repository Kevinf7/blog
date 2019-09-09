from flask import render_template, redirect, url_for, request, jsonify, session
from app.test import bp
import braintree
from app.test.gateway import generate_client_token, transact, find_transaction
from flask_login import login_required
import time


# Card number: 4111 1111 1111 1111
# Expiry: 09/20
# CVV: 400
# Postal Code: 40000


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]


@bp.route('/shop', methods=['GET'])
@login_required
def shop():
    return render_template('test/shop.html')


@bp.route('/checkout/new', methods=['GET'])
@login_required
def new_checkout():
    client_token = generate_client_token()
    return render_template('test/new_checkout.html',client_token=client_token)


@bp.route('/checkouts/<transaction_id>', methods=['GET'])
@login_required
def show_checkout(transaction_id):
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
    return render_template('test/show_checkout.html', transaction=transaction, result=result)


@bp.route('/checkout', methods=['POST'])
@login_required
def create_checkout():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('test.show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors:
            flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('test.new_checkout'))


@bp.route('/add_cart', methods=['POST'])
@login_required
def add_cart():
    # time.sleep(1)
    if 'cart' not in session:
        session['cart'] = []
    item = {
        'id' : request.form['id'],
        'qty' : request.form['qty'],
        'price' : request.form['price']
    }
    session['cart'].append(item)
    session.modified = True
    print(session['cart'])
    return jsonify({'count': len(session['cart'])})


@bp.route('/remove_cart/<id>', methods=['GET'])
@login_required
def remove_cart(id):
    # id in url is index of the session variable cart
    del session['cart'][int(id)]
    session.modified=True
    return redirect(url_for('test.cart'))


@bp.route('/cart', methods=['GET'])
@login_required
def cart():
    if 'cart' not in session:
        session['cart'] = []
    return render_template('test/cart.html',cart=session['cart'])


@bp.route('/clear_cart', methods=['GET'])
@login_required
def clear_cart():
    session.pop('cart', None)
    return ('', 204)
