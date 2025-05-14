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
INSERT INTO recipes (name, category, country, time, difficulty, description, image, calories, proteins, carbs, fats)
VALUES ('Ratatouille', 'Dinner', 'France', 60, 'Medium', 
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

-- maroc
-- Moroccan Lentil & Chickpea Soup (Harira)
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