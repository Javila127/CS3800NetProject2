from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

items = {
    'item1': {'name': 'Item 1', 'price': 10.99},
    'item2': {'name': 'Item 2', 'price': 20.99},
    'item3': {'name': 'Item 3', 'price': 30.99}
}

@app.route('/')
def home():
    return render_template('home.html', items=items)

@app.route('/add_to_cart/<item_key>', methods=['POST'])
def add_to_cart(item_key):
    if 'cart' not in session:
        session['cart'] = {}

    quantity = int(request.form['quantity'])
    if item_key in session['cart']:
        session['cart'][item_key] += quantity
    else:
        session['cart'][item_key] = quantity

    session.modified = True  
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    total_cost = sum(items[key]['price'] * quantity for key, quantity in session.get('cart', {}).items())
    return render_template('cart.html', cart=session.get('cart', {}), items=items, total_cost=total_cost)

@app.route('/confirmation')
def confirmation():
    total_cost = sum(items[key]['price'] * quantity for key, quantity in session.get('cart', {}).items())
    return render_template('confirmation.html', total_cost=total_cost)

@app.route('/confirm_order')
def confirm_order():
    session.pop('cart', None)
    return render_template('order_received.html')

@app.route('/cancel_order')
def cancel_order():
    session.pop('cart', None)
    return redirect(url_for('home'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
