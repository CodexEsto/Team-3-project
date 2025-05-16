-- Active: 1746462800040@@127.0.0.1@3306@recipe_db
CREATE DATABASE IF NOT EXISTS recipe_db;

USE recipe_db;

-- Création de la table principale des recettes
CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    time INT NOT NULL,
    difficulty ENUM('easy', 'Medium', 'hard') NOT NULL,
    description TEXT,
    image VARCHAR(255) NOT NULL,
    calories INT,
    proteins INT,
    carbs INT,
    fats INT
);

-- Création de la table des ingrédients
CREATE TABLE ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    ingredient_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
); 

-- Création de la table des étapes de préparation
CREATE TABLE preparation_steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL,
    step_number INT NOT NULL,
    etape TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE
); 

-- france 
-- (Ratatouille)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
VALUES ('Ratatouille', 'Lunch', 'France', 60, 'Medium', 
'A Mediterranean vegetable stew simmered with olive oil and Provencal herbs.',
'uploads/ratatouille.png', 200, 4, 25, 10);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 2, 'piece', 'zucchini'),
(@recipe_id, 2, 'piece', 'eggplants'),
(@recipe_id, 3, 'piece', 'tomatoes'),
(@recipe_id, 1, 'piece', 'red onion'),
(@recipe_id, 4, 'tablespoons', 'olive oil'),
(@recipe_id, 1, 'teaspoon', 'Provencal herbs'),
(@recipe_id, 1, 'pinch', 'salt and pepper');
INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Cut all vegetables into dices or slices.'),
(@recipe_id, 2, 'Sauté the onion in olive oil.'),
(@recipe_id, 3, 'Add vegetables one by one, starting with eggplants.'),
(@recipe_id, 4, 'Season with herbs, salt, and pepper.'),
(@recipe_id, 5, 'Simmer covered for 40 minutes.');

-- (Boeuf Bourguignon)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
VALUES ('Boeuf Bourguignon', 'Lunch', 'France', 180, 'Medium',
 'Classic French beef stew cooked in red wine', 'uploads/Boeuf_Bourguignon.jpg', 550, 40, 30, 28);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 1.5, 'kg', 'Beef chuck'),
(@recipe_id, 750, 'ml', 'Bourgogne red wine'),
(@recipe_id, 200, 'g', 'Bacon lardons'),
(@recipe_id, 2, 'tbsp', 'Flour'),
(@recipe_id, 4, 'cloves', 'Garlic'),
(@recipe_id, 300, 'g', 'Button mushrooms'),
(@recipe_id, 20, 'small', 'Pearl onions');
INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Marinate beef in wine overnight with carrots and onions'),
(@recipe_id, 2, 'Pat dry meat and brown in a Dutch oven'),
(@recipe_id, 3, 'Cook bacon until crispy, then sauté mushrooms'),
(@recipe_id, 4, 'Deglaze pan with marinade liquid and add bouquet garni'),
(@recipe_id, 5, 'Simmer covered in oven at 160°C for 3 hours');

--(Chocolate Éclair)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
VALUES ('Chocolate Éclair', 'Desserts', 'France', 120, 'hard',
 'Choux pastry filled with cream and topped with chocolate glaze', 'uploads/eclair.jpg', 400, 8, 50, 20);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 125, 'g', 'Butter'),
(@recipe_id, 250, 'ml', 'Water'),
(@recipe_id, 150, 'g', 'All-purpose flour'),
(@recipe_id, 4, 'pieces', 'Eggs'),
(@recipe_id, 200, 'ml', 'Heavy cream'),
(@recipe_id, 100, 'g', 'Dark chocolate');
INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Melt butter in water and bring to a boil'),
(@recipe_id, 2, 'Add flour and stir until dough forms a ball'),
(@recipe_id, 3, 'Cool slightly and add eggs one by one'),
(@recipe_id, 4, 'Pipe onto baking sheet and bake until golden'),
(@recipe_id, 5, 'Fill with cream and glaze with melted chocolate');

-- maroc
-- (Harira)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
VALUES ('Harira Soup', 'Soup', 'Morocco', 60, 'medium', 
'A traditional Moroccan soup with lentils, chickpeas and aromatic spices, often served during Ramadan.',
'uploads/harira.jpg', 250, 10, 35, 8);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 200, 'g', 'dried lentils'),
(@recipe_id, 150, 'g', 'cooked chickpeas'),
(@recipe_id, 1, 'piece', 'large onion'),
(@recipe_id, 3, 'piece', 'ripe tomatoes'),
(@recipe_id, 2, 'tablespoons', 'tomato paste'),
(@recipe_id, 1, 'teaspoon', 'ground turmeric'),
(@recipe_id, 1, 'teaspoon', 'ground ginger'),
(@recipe_id, 0.5, 'teaspoon', 'ground cinnamon'),
(@recipe_id, 1, 'bunch', 'fresh cilantro'),
(@recipe_id, 1, 'bunch', 'fresh parsley'),
(@recipe_id, 2, 'liters', 'vegetable broth');
INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Soak lentils in water for 30 minutes. Drain and rinse.'),
(@recipe_id, 2, 'Sauté chopped onion in olive oil until translucent.'),
(@recipe_id, 3, 'Add grated tomatoes, tomato paste, and spices. Cook 5 minutes.'),
(@recipe_id, 4, 'Add lentils, chickpeas, and broth. Bring to a boil.'),
(@recipe_id, 5, 'Simmer covered for 40 minutes until lentils are tender.'),
(@recipe_id, 6, 'Stir in chopped cilantro and parsley before serving.'),
(@recipe_id, 7, 'Serve with lemon wedges and crusty bread.');

--(shebakiya)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
 VALUES ('Chebakia', 'Dessert', 'Morocco', 150, 'hard',
'Sesame-coated rose-shaped cookies with honey', 'uploads/chebakia.png', 320, 5, 45, 12);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 4, 'cups', 'All-purpose flour'),
(@recipe_id, 1, 'tbsp', 'Sesame seeds'),
(@recipe_id, 1, 'tsp', 'Ground anise'),
(@recipe_id, 1, 'cup', 'Unsalted butter'),
(@recipe_id, 2, 'cups', 'Honey'),
(@recipe_id, 1, 'tbsp', 'Orange blossom water');
INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Mix flour with spices and butter to make dough'),
(@recipe_id, 2, 'Roll dough into thin ropes and form rose shapes'),
(@recipe_id, 3, 'Fry in hot oil until golden brown'),
(@recipe_id, 4, 'Dip in warm honey syrup'),
(@recipe_id, 5, 'Sprinkle with sesame seeds and let cool');

-- (tajine)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats) VALUES
('Chicken Tagine with Olives and Lemon', 'Lunch', 'Morocco', 90, 'Medium',
 'Classic Moroccan chicken dish with preserved lemons and green olives', 'uploads/tagine.jpg', 450, 35, 20, 25);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 1, 'kg', 'Chicken, cut into pieces'),
(@recipe_id, 2, 'cups', 'Green olives, pitted'),
(@recipe_id, 1, 'piece', 'Preserved lemon, quartered'),
(@recipe_id, 2, 'tbsp', 'Olive oil'),
(@recipe_id, 1, 'tsp', 'Ground ginger'),
(@recipe_id, 1, 'tsp', 'Ground cumin'),
(@recipe_id, 1, 'tsp', 'Paprika'),
(@recipe_id, 1, 'bunch', 'Fresh cilantro and parsley');
INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Heat olive oil in a tagine or heavy pot.'),
(@recipe_id, 2, 'Brown chicken pieces on all sides.'),
(@recipe_id, 3, 'Add spices and mix well.'),
(@recipe_id, 4, 'Add olives and preserved lemon.'),
(@recipe_id, 5, 'Cover and simmer for 45 minutes until chicken is tender.');



-- japon
-- (Matcha Mochi)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
VALUES ('Matcha Mochi', 'Desserts', 'Japon', 60, 'Medium',
 'Sweet rice cake flavored with matcha green tea powder', 'uploads/mochi.jpg', 200, 4, 40, 1);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 200, 'g', 'Sweet rice flour (mochi flour)'),
(@recipe_id, 50, 'g', 'Sugar'),
(@recipe_id, 1, 'tbsp', 'Matcha green tea powder'),
(@recipe_id, 200, 'ml', 'Water'),
(@recipe_id, 50, 'g', 'Cornstarch for dusting');
INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Mix sweet rice flour, sugar, and matcha in a bowl.'),
(@recipe_id, 2, 'Gradually add water and stir until smooth.'),
(@recipe_id, 3, 'Steam the mixture for about 20 minutes until cooked.'),
(@recipe_id, 4, 'Dust a surface with cornstarch and transfer the mochi.'),
(@recipe_id, 5, 'Knead gently and shape into small balls or discs.');

--(Tonkatsu Ramen)
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
VALUES ('Tonkatsu Ramen', 'Anime', 'Japon', 120, 'hard',
 'Japanese noodle soup with pork cutlet and rich broth', 'uploads/tonkatsu.jpg', 600, 35, 70, 20);
SET @recipe_id := LAST_INSERT_ID();
INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name) VALUES
(@recipe_id, 1.5, 'kg', 'Pork bones (neck/leg)'),
(@recipe_id, 2, 'liters', 'Water'),
(@recipe_id, 200, 'g', 'Pork belly'),
(@recipe_id, 4, 'servings', 'Ramen noodles'),
(@recipe_id, 4, 'tbsp', 'Soy sauce'),
(@recipe_id, 2, 'tbsp', 'Mirin'),
(@recipe_id, 1, 'tbsp', 'Sesame oil'),
(@recipe_id, 4, 'cloves', 'Garlic'),
(@recipe_id, 2, 'inch', 'Ginger'),
(@recipe_id, 1, 'piece', 'Kombu seaweed'),
(@recipe_id, 4, 'units', 'Soft-boiled eggs'),
(@recipe_id, 100, 'g', 'Bamboo shoots'),
(@recipe_id, 4, 'sheets', 'Nori'),
(@recipe_id, 1, 'cup', 'Bean sprouts'),
(@recipe_id, 4, 'tbsp', 'Tonkatsu sauce'),
(@recipe_id, 1, 'tsp', 'Chili oil (optional)');

INSERT INTO preparation_steps (recipe_id, step_number, etape) VALUES
(@recipe_id, 1, 'Make broth: Boil pork bones 10min, discard water. Add 2L fresh water, simmer 8 hours with garlic, ginger and kombu'),
(@recipe_id, 2, 'Prepare chashu pork: Roll pork belly, brown in pan. Braise in soy sauce, mirin and water for 2 hours'),
(@recipe_id, 3, 'Make tare: Mix 2 cups broth with soy sauce, mirin and sesame oil. Simmer 15min'),
(@recipe_id, 4, 'Cook noodles: Boil ramen noodles 1-2min until al dente, rinse under cold water'),
(@recipe_id, 5, 'Assemble bowls: Add 60ml tare to each bowl, pour hot broth. Add noodles and arrange toppings'),
(@recipe_id, 6, 'Fry tonkatsu: Bread pork cutlet with panko, deep-fry at 180°C until golden'),
(@recipe_id, 7, 'Garnish with soft-boiled egg, nori, bamboo shoots, bean sprouts and chili oil');