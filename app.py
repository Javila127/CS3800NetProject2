from flask import Flask, render_template, redirect, url_for, session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Set a random secret key

# Sample product data
products = {
    1: {'id': 1, 'name': 'Product 1', 'price': 10.99},
    2: {'id': 2, 'name': 'Product 2', 'price': 20.99},
    3: {'id': 3, 'name': 'Product 3', 'price': 30.99}
}

@app.route('/')
def home():
    return render_template('home.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = products.get(product_id)
    if product:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(product)
        session.modified = True
    return redirect(url_for('home'))

@app.route('/cart')
def show_cart():
    return render_template('cart.html', cart=session.get('cart', []))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
