# Recipe Sharing Website

A dynamic recipe sharing platform that allows users to discover, share, and organize culinary recipes from around the world.

## Features

- **User Authentication**: Secure signup and login system
- **Recipe Management**: Add, view, and organize recipes
- **World Cuisine**: Browse recipes by country of origin
- **Category Navigation**: Filter recipes by category (Lunch, Desserts, Vegetarian, etc.)
- **Detailed Recipe Pages**: View ingredients, preparation steps, nutritional information
- **Contact Form**: Get in touch with the site administrators
- **Responsive Design**: Optimized for both desktop and mobile devices

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Email Support**: Flask-Mail
- **Form Handling**: Flask-WTF with CSRF protection

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- Git

### Setup Instructions

1. **Clone the repository**
   ```
   git clone <your-repository-url>
   cd Team-3-project
   ```

2. **Create and activate virtual environment**
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_DEBUG=True
   FLASK_SECRET_KEY=your-secret-key
   CSRF_SECRET_KEY=your-csrf-secret-key
   
   # Database Configuration
   DATABASE_URL=mysql://username:password@localhost/recipe_db
   
   # Email Configuration
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-email-password
   ```

5. **Set up the database**
   ```
   # Connect to MySQL and create the database
   mysql -u root -p
   CREATE DATABASE recipe_db;
   exit
   
   # Import schema and sample data
   mysql -u root -p recipe_db < information.sql
   ```



## Usage

### User Registration and Login
1. Navigate to the signup page to create a new account
2. Verify your email address if verification is enabled
3. Log in with your credentials

### Exploring Recipes
- Browse the home page for featured recipes
- Use the World Cuisine section to discover international dishes
- Navigate categories to find recipes by type

### Adding Recipes
1. Log in to your account
2. Click on "Your Recipes" button
3. Fill out the recipe form with:
   - Basic info (name, category, country, cook time, difficulty)
   - Ingredients list
   - Step-by-step preparation instructions
   - Optional nutritional information
   - Recipe image

### Contact
Use the Contact form to reach out to site administrators for:
- Recipe suggestions
- Technical support
- Partnership inquiries

## Project Structure

```
Team-3-project/
│
├── app.py                  # Main Flask application file
├── information.sql         # Database schema and sample data
├── requirements.txt        # Python dependencies
│
├── static/                 # Static assets
│   ├── css/                # Stylesheets
│   ├── img/                # Images
│   ├── js/                 # JavaScript files
│   └── uploads/            # User uploaded images
│
├── templates/              # HTML templates
│   ├── add-recipe.html     # Recipe addition form
│   ├── contactus.html      # Contact page
│   ├── country_recipes.html # Recipes by country
│   ├── forgot_password.html # Password reset request
│   ├── indext.html         # Home page
│   ├── login.html          # User login
│   ├── recipe_detail.html  # Individual recipe view
│   ├── reset_password.html # Password reset form
│   ├── signup.html         # User registration
│   ├── thank_you.html      # Confirmation page
│   └── WORLD.html          # World cuisine overview
```

