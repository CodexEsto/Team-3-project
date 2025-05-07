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
