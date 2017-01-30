###############################################################################
# Web Technology at VU University Amsterdam
# Assignment 3
#
# The assignment description is available on Blackboard.
# This is a template for you to quickly get started with Assignment 3. Read
# through the code and try to understand it.
#
# Have you looked at the documentation of bottle.py?
# http://bottle.readthedocs.org/en/stable/index.html
#
# Once you are familiar with bottle.py and the assignment, start implementing
# an API according to your design by adding routes.
###############################################################################

# Include more methods/decorators as you use them
# See http://bottle.readthedocs.org/en/stable/api.html#bottle.Bottle.route
from bottle import response, request, error, get, put, post, delete
import json


###############################################################################
#
# Routes
#
###############################################################################

# Gets all the products in the inventory.
@get('/products')
def db_example(db):

    # Get all products from the database or empty array if none exist.
    db.execute('SELECT * FROM inventory')

    # Get all results in a list of dictionaries.
    products = db.fetchall()

    if (products == []):
        # If the product is not found respond to client with an error.
        response.status = 404
        response.headers['Content-Type'] = 'application/json'
        response_body = {'status': 'Not Found', 'message': 'No products have been found in our database.'}
    else:
        # Set the 200 status code if 1 or more products is found inside the database.
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        response_body = products

    response.body = json.dumps(response_body)
    return response

# Gets a specific product in the inventory.
@get('/products/<id>')
def db_example(db, id):

    # Get the product from the database or an empty array if is does not exist.
    db.execute('SELECT * from inventory where id={}'.format(id))
    product = db.fetchall()

    if (product == []):
        # If the product is not found respond to client with an error.
        response.status = 404
        response.headers['Content-Type'] = 'application/json'
        response_body = {'status': 'Not Found', 'message': 'The product you are looking for could not be found.'}
    else:
        # Set the 200 status code if the product is found.
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        response_body = product[0]

    response.body = json.dumps(response_body)
    return response

# Adds a new product to the inventory.
@post('/products')
def db_example(db):

    # Get the data fields form the request.
    name = request.json.get('name')
    category = request.json.get('category')
    amount = request.json.get('amount')
    location = request.json.get('location')
    date = request.json.get('date')

    if (not name or not category or not amount or not location or not date):
        # If some parameters to are missing respont with an error to the client.
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        response_body = {'status': 'Bad Request', 'message': 'One or more parameters in your request are missing.'}
    else:
        # Insert the product into the database.
        db.execute('INSERT INTO inventory (name, category, amount, location, date) VALUES (?, ?, ?, ?, ?)', (name, category, amount, location, date))

        # Gets the new product id by getting the last row's id.
        id = db.lastrowid

        # Save the host ip of the host.
        host = request.get_header('host')

        # Set the 201 status code to let the user know that the product has been succefully added to the database.
        response.status = 201
        response.headers['Content-Type'] = 'application/json'

        # Creates the URL for the newly added product.
        response_body = {'url': 'http://{}/products/{}'.format(host,id)}

    response.body = json.dumps(response_body)
    return response

# Changes an existing product in the inventory.
@put('/products/<id>')
def db_example(db, id):

    # Get the data fields form the request.
    name = request.json.get('name')
    category = request.json.get('category')
    amount = request.json.get('amount')
    location = request.json.get('location')
    date = request.json.get('date')

    if (not name or not category or not amount or not location or not date):
        # If some parameters to are missing respont with an error to the client.
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        response_body = {'status': 'Bad Request', 'message': 'One or more parameters in your request are missing.'}
    else:
        # Get the product from the database or empty array if is does not exist.
        db.execute("SELECT id from inventory WHERE id={}".format(id))
        product = db.fetchall()

        if (product == []):
            # If the product is not found respond to client with an error.
            response.status = 404
            response.headers['Content-Type'] = 'application/json'
            response_body = {'status': 'Not Found', 'message': 'The product you are looking for could not be found.'}
        else:
            # Update the data in the database.
            db.execute('UPDATE inventory SET name = "{}", category = "{}", amount = "{}", location = "{}", date = "{}" WHERE id={}'.format(name, category, amount, location, date, id))

            # Respond to the client with the newly added product.
            response.status = 200
            response.headers['Content-Type'] = 'application/json'
            response_body = request.json

    response.body = json.dumps(response_body)
    return response

# Deletes a product form the inventory.
@delete('/products/<id>')
def db_example(db, id):

    # Get the product from the database or empty array if is does not exist.
    db.execute("SELECT id from inventory WHERE id={}".format(id))
    product = db.fetchall()

    if (product == []):
        # If the product is not found respond to client with an error.
        response.status = 404
        response.headers['Content-Type'] = 'application/json'
        response_body = {'status': 'Not Found', 'message': 'The product you are looking for could not be found.'}
        response.body = json.dumps(response_body)
    else:
        db.execute('DELETE from inventory WHERE id={}'.format(id))

        # Respond with a 204 message to notify the clinet that the product is succesfully deleted.
        response.status = 204
        response.headers['Content-Type'] = 'application/json'
        response.body = ''

    return response


###############################################################################
#
# Error handling
#
###############################################################################

@error(404)
def error_404_handler(e):

    # Content type must be set manually in error handlers.
    response.headers['Content-Type'] = 'application/json'

    return json.dumps({'Error': {'Message': e.status_line, 'Status': e.status_code}})


###############################################################################
# This starts the server
#
# Access it at http://localhost:8080
#
# If you have problems with the reloader (i.e. your server does not
# automatically reload new code after you save this file), set `reloader=False`
# and reload manually.
#
# You might want to set `debug=True` while developing and/or debugging and to
# `False` before you submit.
#
# The installed plugin 'WtPlugin' takes care of enabling CORS (Cross-Origin
# Resource Sharing; you need this if you use your API from a website) and
# provides you with a database cursor.
###############################################################################

if __name__ == "__main__":
    from bottle import install, run
    from wtplugin import WtDbPlugin, WtCorsPlugin

    install(WtDbPlugin())
    install(WtCorsPlugin())
    run(host='localhost', port=8080, reloader=True, debug=True, autojson=False)
