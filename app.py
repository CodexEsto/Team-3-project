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
    try:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
            
        form = {
            'email': request.form.get('email', '')
        }
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            ip_address = get_client_ip(request)
            
            # Validate email
            is_valid, message = validate_email(email)
            if not is_valid:
                flash(message, 'error')
                return render_template('login.html', form=form)
            
            try:
                # Check login attempts
                if LoginAttempt.check_attempts(email, ip_address):
                    flash('Too many failed attempts. Please try again later.', 'error')
                    return render_template('login.html', form=form)
                
                # Find user
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
            except Exception as e:
                logger.error(f"Database error during login: {str(e)}")
                flash('An error occurred. Please try again.', 'error')
                return render_template('login.html', form=form)
                
        return render_template('login.html', form=form)
    except Exception as e:
        logger.error(f"Unexpected error in login route: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return render_template('login.html', form={'email': ''})

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

def generate_reset_token():
    return serializer.dumps(str(datetime.utcnow().timestamp()))

def send_password_reset_email(user, token):
    reset_url = url_for('reset_password', token=token, _external=True)
    try:
        msg = Message('Password Reset Request',
                    sender=app.config['MAIL_DEFAULT_SENDER'],
                    recipients=[user.email])
        msg.body = f"""To reset your password, visit the following link:

{reset_url}

If you did not make this request, simply ignore this email and no changes will be made.

This link will expire in 30 minutes.
"""
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        return False

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            try:
                # Generate token
                token = generate_reset_token()
                
                # Save reset token
                reset_record = PasswordReset(
                    user_id=user.id,
                    token=token,
                    expires_at=datetime.utcnow() + timedelta(minutes=30)
                )
                db.session.add(reset_record)
                db.session.commit()
                
                # Send email
                if send_password_reset_email(user, token):
                    flash('Password reset instructions have been sent to your email.', 'success')
                else:
                    db.session.delete(reset_record)
                    db.session.commit()
                    flash('Error sending reset email. Please try again.', 'error')
            except Exception as e:
                logger.error(f"Error in forgot password: {str(e)}")
                db.session.rollback()
                flash('An error occurred. Please try again.', 'error')
        else:
            # For security, don't reveal if email exists
            flash('Password reset instructions have been sent if the email exists.', 'success')
            
        return redirect(url_for('login'))
        
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    # Verify token
    reset_record = PasswordReset.query.filter_by(
        token=token,
        used=False
    ).filter(PasswordReset.expires_at > datetime.utcnow()).first()
    
    if not reset_record:
        flash('Invalid or expired reset link.', 'error')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html')
            
        is_valid, message = User.validate_password(password)
        if not is_valid:
            flash(message, 'error')
            return render_template('reset_password.html')
            
        try:
            # Update password
            user = User.query.get(reset_record.user_id)
            user.set_password(password)
            
            # Mark token as used
            reset_record.used = True
            
            db.session.commit()
            flash('Your password has been updated! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error resetting password: {str(e)}")
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return render_template('reset_password.html')
            
    return render_template('reset_password.html')

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

@app.route('/profile')
@login_required
def profile():
    # Get user's recipes
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM recipes WHERE user_id = %s ORDER BY id DESC", (current_user.id,))
    user_recipes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('profile.html', user=current_user, recipes=user_recipes)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')  # Added phone field
        subject = request.form.get('subject', '')  # Added subject field
        message = request.form.get('message')
        
        # Send email
        try:
            msg = Message(f'New Contact Form: {subject}',
                        sender=app.config['MAIL_DEFAULT_SENDER'],
                        recipients=[app.config['ADMIN_EMAIL']])
            msg.body = f"""
            Name: {name}
            Email: {email}
            Phone: {phone}
            Subject: {subject}
            Message: {message}
            """
            mail.send(msg)
            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            logger.error(f"Error sending contact email: {str(e)}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
        
        return redirect(url_for('contact'))
    return render_template('contactus.html')


@app.route('/search')
def search_recipes():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Search in recipe names and descriptions
    search_term = f"%{query}%"
    cursor.execute("""
        SELECT * FROM recipes 
        WHERE name LIKE %s 
        OR description LIKE %s 
        OR category LIKE %s
        OR country LIKE %s
    """, (search_term, search_term, search_term, search_term))
    
    recipes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('search_results.html', recipes=recipes, query=query)

# Database initialization
def init_db():
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Check if admin user exists
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                # Create admin user
                admin = User(
                    fullname='Admin User',
                    email='admin@example.com',
                    is_active=True,
                    is_verified=True
                )
                admin.set_password('Admin@123')
                db.session.add(admin)
                db.session.commit()
                logger.info("Admin user created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    init_db()  # Initialize database before running the app
    app.run(debug=app.config['FLASK_DEBUG'])