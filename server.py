#!/usr/bin/env python3

import cgi

# Function to parse form data
def get_form_data():
    form = cgi.FieldStorage()
    item = form.getvalue('item')
    return item

# Function to render the HTML response
def render_html(item):
    print("Content-Type: text/html")
    print()
    print("<!DOCTYPE html>")
    print("<html>")
    print("<head>")
    print("<title>Shopping Cart</title>")
    print("</head>")
    print("<body>")
    print("<h1>Shopping Cart</h1>")
    print("<p>Item added to cart: {}</p>".format(item))
    print("</body>")
    print("</html>")

if __name__ == "__main__":
    item = get_form_data()
    render_html(item)
