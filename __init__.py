from flask import Flask , jsonify , Blueprint, request
import routes as route
app = Flask(__name__)
app.register_blueprint(route.bp)
if __name__ == '__main__':
    app.run(debug=True)