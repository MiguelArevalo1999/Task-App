from flask import  request,make_response, redirect, render_template, json,session,url_for,flash
from werkzeug.exceptions import HTTPException, InternalServerError
from flask_bootstrap import Bootstrap 
import unittest
from app import create_app
from app.forms import LoginForm


app = create_app()


todos = ['Comprar café','Enviar solicitud de compra','Entregar video']


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
        })
    response.content_type = "application/json"
    return response

 
@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return render_template("500.html"), 500

    # wrapped unhandled error
    return render_template("500_unhandled.html", e=original), 500

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response

@app.route('/hello', methods=['GET'])
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
            'user_ip' : user_ip,
            'todos' : todos,
            'username' : username
            }
 
    return render_template('hello.html', **context)
