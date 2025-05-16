import os
import re
from datetime import datetime, timedelta
import logging
from flask import Flask, redirect, url_for, render_template, request, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect
import mysql.connector
from jinja2 import ChoiceLoader, FileSystemLoader

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration des dossiers de templates
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,  # Le chargeur par défaut (templates/)
    FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), ''))  # Dossier racine du projet
])

# Configuration
class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Configuration for Recipes
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'salmabbdll6@gmail.com'
    MAIL_PASSWORD = 'urxj joko ysuj qykl'
    MAIL_DEFAULT_SENDER = 'salmabbdll6@gmail.com'
    ADMIN_EMAIL = 'salmabbdll6@gmail.com'
    
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)
    WTF_CSRF_SECRET_KEY = os.getenv('CSRF_SECRET_KEY', 'your-csrf-secret-key')

app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL Configuration for Recipes
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'recipe_db'
}

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test email configuration
try:
    with app.app_context():
        mail.connect()
        logger.info("Email configuration test successful")
except Exception as e:
    logger.error(f"Email configuration error: {str(e)}")

# Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        if not any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
            return False, "Password must contain at least one special character"
        return True, ""

class PasswordReset(db.Model):
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    success = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def check_attempts(cls, email, ip_address, window_minutes=30, max_attempts=5):
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        attempts = cls.query.filter(
            cls.email == email,
            cls.ip_address == ip_address,
            cls.success == False,
            cls.created_at >= cutoff
        ).count()
        return attempts >= max_attempts

# Utility functions
def validate_email(email):
    if not email:
        return False, "Email is required"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    if len(email) > 120:
        return False, "Email is too long (maximum 120 characters)"
    return True, ""

def validate_fullname(fullname):
    if not fullname:
        return False, "Full name is required"
    fullname = " ".join(fullname.split())
    if len(fullname) < 2:
        return False, "Full name is too short"
    if len(fullname) > 100:
        return False, "Full name is too long (maximum 100 characters)"
    if not re.match(r'^[a-zA-Z\s\'-]+$', fullname):
        return False, "Full name can only contain letters, spaces, hyphens, and apostrophes"
    if len(fullname.split()) < 2:
        return False, "Please provide both first and last name"
    return True, ""

def get_client_ip(request):
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes - Authentication
@app.route('/')
def index():
    return render_template('indext.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = {
        'email': request.form.get('email', '')
    }
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        ip_address = get_client_ip(request)
        
        if LoginAttempt.check_attempts(email, ip_address):
            flash('Too many failed attempts. Please try again later.', 'error')
            return render_template('login.html', form=form)
            
        is_valid, message = validate_email(email)
        if not is_valid:
            flash(message, 'error')
            return render_template('login.html', form=form)
            
        user = User.query.filter_by(email=email).first()
        attempt = LoginAttempt(email=email, ip_address=ip_address)
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'error')
                return render_template('login.html', form=form)
                
            attempt.success = True
            db.session.add(attempt)
            user.update_last_login()
            login_user(user)
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        
        db.session.add(attempt)
        db.session.commit()
        flash('Invalid email or password.', 'error')
        return render_template('login.html', form=form)
        
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = {
        'fullname': request.form.get('fullname', ''),
        'email': request.form.get('email', ''),
    }
    
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        is_valid, message = validate_fullname(fullname)
        if not is_valid:
            flash(message, 'error')
            return render_template('signup.html', form=form)
            
        is_valid, message = validate_email(email)
        if not is_valid:
            flash(message, 'error')
            return render_template('signup.html', form=form)
            
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html', form=form)
            
        is_valid, message = User.validate_password(password)
        if not is_valid:
            flash(message, 'error')
            return render_template('signup.html', form=form)
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('signup.html', form=form)
            
        user = User(fullname=fullname, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return render_template('signup.html', form=form)
            
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Routes - Recipe Management
@app.route('/add-recipe')
@login_required
def add_recipe_form():
    return render_template('add-recipe.html')

@app.route('/world-cuisine')
def world_cuisine():
    return render_template('WORLD.html')

@app.route('/addrecipe/submit', methods=['POST'])
@login_required
def submit_recipe():
    if request.method == 'POST':
        # les données principales
        name = request.form['name']
        category = request.form['category']
        country = request.form.get('country', '')
        time = request.form['time']
        difficulty = request.form['difficulty']
        description = request.form.get('description', '')
        calories = int(request.form.get('calories')) if request.form.get('calories') else None
        proteins = int(request.form.get('proteins')) if request.form.get('proteins') else None
        carbs = int(request.form.get('carbs')) if request.form.get('carbs') else None
        fats = int(request.form.get('fats')) if request.form.get('fats') else None
        
        # image
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            db_image_path = 'uploads/' + filename
           
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # recette
        insert_recipe = """
        INSERT INTO recipes 
        (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        recipe_data = (name, category, country, time, difficulty, description, db_image_path, calories, proteins, carbs, fats)
        cursor.execute(insert_recipe, recipe_data)
        recipe_id = cursor.lastrowid  
        
        # ingrédients
        quantities = request.form.getlist('quantity[]')
        units = request.form.getlist('unit[]')
        ingredient_names = request.form.getlist('ingredient_name[]')
        
        for i in range(len(ingredient_names)):
            if ingredient_names[i]:  
                insert_ingredient = """
                INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name)
                VALUES (%s, %s, %s, %s)
                """
                ingredient_data = (recipe_id, quantities[i], units[i], ingredient_names[i])
                cursor.execute(insert_ingredient, ingredient_data)
        
        # préparation
        prep_steps = request.form.getlist('preparation_step[]')
        for i, step in enumerate(prep_steps, 1):
            if step:  
                insert_step = """
                INSERT INTO preparation_steps (recipe_id, step_number, etape)
                VALUES (%s, %s, %s)
                """
                preparation_data = (recipe_id, i, step)
                cursor.execute(insert_step, preparation_data)
        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Récupérer les détails de la recette
    cursor.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
    recipe = cursor.fetchone()
    
    # Récupérer les ingrédients
    cursor.execute("SELECT * FROM ingredients WHERE recipe_id = %s", (recipe_id,))
    ingredients = cursor.fetchall()
    
    # Récupérer les étapes de préparation
    cursor.execute("SELECT * FROM preparation_steps WHERE recipe_id = %s ORDER BY step_number", (recipe_id,))
    steps = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('recipe_detail.html', recipe=recipe, ingredients=ingredients, steps=steps)

@app.route('/country/<country_name>')
def country_recipes(country_name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Récupérer les recettes du pays spécifié
    cursor.execute("SELECT * FROM recipes WHERE country = %s", (country_name,))
    recipes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('country_recipes.html', country=country_name, recipes=recipes)

# Database initialization
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=app.config['FLASK_DEBUG'])