#!/usr/bin/env python3

import cgi
import os
import urllib.parse

# Function to parse form data
def get_form_data():
    form = cgi.FieldStorage()
    item = form.getvalue('item')
    quantity = int(form.getvalue('quantity'))
    return item, quantity

# Function to render the HTML response
def render_html(html_content):
    print("Content-Type: text/html")
    print()
    print(html_content)

# Function to read cart contents from file
def read_cart():
    if not os.path.exists("cart.txt"):
        return {}
    with open("cart.txt", "r") as file:
        lines = file.readlines()
        cart = {}
        for line in lines:
            item, quantity = line.strip().split(":")
            cart[item] = int(quantity)
        return cart

# Function to write cart contents to file
def write_cart(cart):
    with open("cart.txt", "w") as file:
        for item, quantity in cart.items():
            file.write(f"{item}:{quantity}\n")

if __name__ == "__main__":
    form_item, form_quantity = get_form_data()

    if form_item:
        cart = read_cart()
        cart[form_item] = cart.get(form_item, 0) + form_quantity
        write_cart(cart)
        render_html("<!DOCTYPE html><html><head><title>Added to Cart</title></head><body><h1>Item Added to Cart</h1><p><a href='index.html'>Continue Shopping</a></p></body></html>")
    else:
        # Redirect to the index page if no item is specified
        print("Location: index.html")
        print()

