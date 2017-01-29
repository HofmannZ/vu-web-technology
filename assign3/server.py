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
from bottle import response, error, get
import json


###############################################################################
# Routes
#
# TODO: Add your routes here and remove the example routes once you know how
#       everything works.
###############################################################################

@get('/hello')
def hello_world():
    '''Responds to http://localhost:8080/hello with an example JSON object
    '''
    response_body = {'Hello': 'World'}

    # This returns valid JSON in the response, but does not yet set the 
    # associated HTTP response header.  This you should do yourself in your 
    # own routes! 
    return json.dumps(response_body)

@get('/db-example')
def db_example(db):
    '''Responds with names of all products in Amsterdam
    
    Add a parameter 'db' to your function to get a database cursor from
    WtPlugin. The parameter db is of type sqlite3.Cursor. Documentation is
    at https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor

    If you want to start with a clean sheet, delete the file 'inventory.db'.
    It will be automatically re-created and filled with one example item.

    Access this route at http://localhost:8080/db-example
    '''
    # Execute SQL statement to select the name of all items located in A'dam
    db.execute("SELECT name FROM inventory WHERE location=?", ('Amsterdam',))

    # Get all results in a list of dictionaries
    names = db.fetchall() # Use db.fetchone() to get results one by one

    # TODO: set the appropriate HTTP headers and HTTP response codes.

    # Return results as JSON
    return json.dumps(names)




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

