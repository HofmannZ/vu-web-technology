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
# Routes
#
# TODO: Add your routes here and remove the example routes once you know how
#       everything works.
###############################################################################


@get('/products')
def db_example(db):
    '''Responds with all the products
    Access this route at http://localhost:8080/products
    '''
    response.headers['Content-Type'] = 'application/json'
    # Execute SQL statement to select all the products from the database
    db.execute("SELECT * FROM inventory ")
    # Get all results in a list of dictionaries
    products = db.fetchall() # Use db.fetchone() to get results one by one
    if (products == []):
        # Set the 404 status code if the database is empty
        response.status = 404
        response_body = { "status": "Not Found", "message": "No product has been found",}
        response.body = json.dumps(response_body)
    else:
        # Set the 200 status code if 1 or more products is found inside the database
        response.status = 200
        response.body = json.dumps(names)

    return response

@get('/products/<id>')
def db_example(db, id):
    '''Responds with the requested product if exists
    Access this route at http://localhost:8080/products/<id>
    '''
    response.headers['Content-Type'] = 'application/json'
    # Execute SQL statement to select the desired product
    # Get the product or emplty array if not existent
    db.execute("SELECT * from inventory where id={}".format(id))
    product = db.fetchall() # Use db.fetchone() to get the result
    if (product == []):
        # Set the 404 status code if the product is not found
        response.status = 404
        response_body = { "status": "Not Found", "message": "Product with the provided id is not existent",}
    else:
        # Set the 302 status code if the product is found
        response.status = 302
        response_body = product
    response.body = json.dumps(response_body)

    return response

@put('/products/<id>')
def db_example(db, id):
    '''Responds with the requested product if exists
    Access this route at http://localhost:8080/products/<id>
    '''
    # Execute SQL statement to select the desired product
    # Get the product or emplty array if not existent
    db.execute("SELECT id from inventory WHERE id={}".format(id))
    data = db.fetchall()
    if (data == []):
        # Set the 404 status code if the product is not found
        response.status = 404
        response_body = { "status": "Not Found", "message": "Product with the provided id is not existent",}
        response.body= json.dumps(response_body)
    else:
        # Deconstruct each field from the Request JSON
        requestedData = request.json
        name = request.json.get('name')
        category = request.json.get('category')
        amount = request.json.get('amount')
        location = request.json.get('location')
        date = request.json.get('date')
        # Create the SQL query using the data from the request
        db.execute('UPDATE inventory SET name = "{}", category = "{}", amount = "{}", location = "{}", date = "{}" WHERE id={}'.format(name, category, amount, location, date, id))
        # Set the 200 code when the SQL query is executed
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        response.body= json.dumps(requestedData)

    return response

@delete('/products/<id>')
def db_example(db, id):
    '''Responds with the 204 status code if the product is deleted
    Access this route at http://localhost:8080/products/<id>
    '''
    response.headers['Content-Type'] = 'application/json'
    # Execute SQL statement to select the desired product
    db.execute("SELECT id from inventory WHERE id={}".format(id))
    data = db.fetchall()
    if (data == []):
        # Set the 404 status code if the product is not found
        response.status = 404
        response_body = { "status": "Not Found", "message": "Product with the provided id is not existent",}
        response.body = json.dumps(response_body)
    else:
        db.execute("DELETE from inventory WHERE id={}".format(id))
        # Set the 204 code when the SQL query is executed
        response.status = 204
        response.body = ''

    return response

@post('/products')
def db_example(db):
    '''Add a new product in the database
    Access this route at http://localhost:8080/products
    '''
    # Deconstruct each field from the Request JSON
    requestedData = request.json
    name = request.json.get('name')
    category = request.json.get('category')
    amount = request.json.get('amount')
    location = request.json.get('location')
    date = request.json.get('date')
    # Create the SQL query using the data from the request
    db.execute('INSERT INTO inventory (name,category,amount,location,date) VALUES (?,?,?,?,?)',(name,category,amount,location,date))
    # Gets the new product id by getting the last row's id
    id = db.lastrowid
    # Save the host ip and password
    host = request.get_header('host')
    # Concatentes the string for the newly added product
    response_body = {'url': 'http://{}/products/{}'.format(host,id)}
    # Set the 201 status code after the product is added
    response.status = 201
    response.headers['Content-Type'] = 'application/json'
    response.body = json.dumps(response_body)

    return response





###############################################################################
# Error handling
#
# TODO: Add sensible error handlers for all errors that may occur when a user
#       accesses your API.
###############################################################################

@error(404)
def error_404_handler(e):

    # Content type must be set manually in error handlers
    response.content_type = 'application/json'

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
