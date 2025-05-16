from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'recipe_db'
}

@app.route('/')
def home():
    return render_template('indext.html')

@app.route('/add-recipe')
def add_recipe_form():
    return render_template('add-recipe.html')

@app.route('/world-cuisine')
def world_cuisine():
    return render_template('WORLD.html')

# Récupérer et stocker les données du formulaire
@app.route('/addrecipe/submit', methods=['POST'])
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
        
        #préparation
        prep_steps = request.form.getlist('preparation_step[]')
        for i, step in enumerate(prep_steps, 1):
            if step:  
                insert_step = """
                INSERT INTO preparation_steps (recipe_id, step_number, etape)
                VALUES (%s, %s, %s)
                """
                preparation_data = (recipe_id,i, step)
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
    

if __name__ == '__main__':
    app.run(debug=True)