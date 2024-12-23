from flask import Flask , jsonify , Blueprint, request
import routes as route
from flask_mail import Mail
app = Flask(__name__)
app.register_blueprint(route.bp)
mail = Mail()



if __name__ == '__main__':
    app.run(debug=True)