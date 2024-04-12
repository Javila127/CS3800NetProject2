from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dictionary containing the items available to buy
items = {
    'item1': {'name': 'Item 1', 'price': 10.99},
    'item2': {'name': 'Item 2', 'price': 20.99},
    'item3': {'name': 'Item 3', 'price': 30.99}
}

# Home route - Renders home.html template with items available to buy
@app.route('/')
def home():
    return render_template('home.html', items=items)

# Route for adding items to the cart
@app.route('/add_to_cart/<item_key>', methods=['POST'])
def add_to_cart(item_key):
    if 'cart' not in session:
        session['cart'] = {}

    # Extract quantity from form data
    quantity = int(request.form['quantity'])

    # Add item to cart or update quantity if already in cart
    if item_key in session['cart']:
        session['cart'][item_key] += quantity
    else:
        session['cart'][item_key] = quantity

    session.modified = True  # Mark session as modified
    return redirect(url_for('cart'))

# Route for displaying the cart
@app.route('/cart')
def cart():
    # Calculate total cost of items in the cart
    total_cost = sum(items[key]['price'] * quantity for key, quantity in session.get('cart', {}).items())
    return render_template('cart.html', cart=session.get('cart', {}), items=items, total_cost=total_cost)

# Route for displaying confirmation page
@app.route('/confirmation')
def confirmation():
    # Calculate total cost of items in the cart
    total_cost = sum(items[key]['price'] * quantity for key, quantity in session.get('cart', {}).items())
    return render_template('confirmation.html', total_cost=total_cost)

# Route for confirming order
@app.route('/confirm_order')
def confirm_order():
    # Clear cart upon order confirmation
    session.pop('cart', None)
    return render_template('order_received.html')

# Route for canceling order
@app.route('/cancel_order')
def cancel_order():
    # Clear cart upon order cancellation
    session.pop('cart', None)
    return redirect(url_for('home'))

# Route for clearing the cart
@app.route('/clear_cart')
def clear_cart():
    # Clear cart
    session.pop('cart', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Run the application in debug mode on port 8000
    app.run(debug=True, port = 8000)
