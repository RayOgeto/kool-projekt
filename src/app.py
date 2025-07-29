# this where we'll do our magic 
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import *
from flask_cors import CORS
from flask_login import LoginManager

# Import models and database
from src.models.user import User, db
from src.models.need import Need
from src.models.donation import Donation

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'BBLDRIZZY'

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#db
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'needs.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Register blueprints
from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.routes.need import need_bp
from src.routes.donation import donation_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(need_bp, url_prefix='/api')
app.register_blueprint(donation_bp, url_prefix='/api')

def init_database():
    
    with app.app_context():
        
        db.create_all()
        

#route malanding and redirecting
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "you have not created a static folder part", 404
    
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "bado huna landing page boss", 404
        
        
if __name__ == '__main__':
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=True)