from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
# Use an absolute path for the database to avoid ambiguity
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')
db_dir = os.path.dirname(db_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<Driver {self.email}>'

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing email or password'}), 400

    email = data['email']
    password = data['password']

    if Driver.query.filter_by(email=email).first():
        return jsonify({'message': 'Email address already registered'}), 409

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_driver = Driver(email=email, password_hash=hashed_password)

    db.session.add(new_driver)
    db.session.commit()

    return jsonify({'message': 'New driver registered successfully'}), 201

# The lambda_handler is useful for AWS Lambda deployment.
# It's good practice to keep it.
try:
    import serverless_wsgi
    def lambda_handler(event, context):
        return serverless_wsgi.handle_request(app, event, context)
except ImportError:
    pass

if __name__ == '__main__':
    app.run(debug=True)
