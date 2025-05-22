from flask import Flask
from backend.app.routes.auth import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)