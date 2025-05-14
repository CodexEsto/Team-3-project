// This script is for adding and delete a recipe

let AddIngr = document.getElementById("add-ingredient");
let ingredientsList = document.getElementById("ingredient-list");


AddIngr.onclick = function () {
    let newIngredient = document.createElement("div");
    newIngredient.className = "ingredient-item";
    newIngredient.innerHTML = `
            <input type="text" placeholder="Quantity" class="ingredient-quantity" name="quantity[]" required>
            <input type="text" placeholder="Unit" class="ingredient-unit" name="unit[]" required>
            <input type="text" placeholder="Ingredient" class="ingredient-name" name="ingredient_name[]" required>
            <button type="button" class="remove-ingredient">X</button>`;
    newIngredient.querySelector('.remove-ingredient').addEventListener('click', function () {
        newIngredient.remove();
    });
    ingredientsList.appendChild(newIngredient);

}
// This script is for adding and delete a preparation step

let AddStep = document.getElementById("add-preparation");
let stepsList = document.getElementById("step-list");

AddStep.onclick = function () {
    let newStep = document.createElement("div");
    newStep.className = "preparation-item";
    newStep.innerHTML = `
            <input type="text" placeholder="Step" class="preparation-step" name="preparation_step[]" required>
            <button type="button" class="remove-preparation">X</button>`;
    newStep.querySelector('.remove-preparation').addEventListener('click', function () {
        newStep.remove();
    });
    stepsList.appendChild(newStep);
}

// Form validation on submit
document.getElementById("recipe-form").onsubmit = function () {
    let recipeName = document.getElementById("name").value.trim();
    let time = document.getElementsByName("time")[0].value.trim();
    let difficulty = document.getElementsByName("difficulty")[0].value;
    let image = document.getElementById("image").value;
    let category = document.getElementsByName("category")[0].value;
    let ingredientItems = document.getElementsByClassName("ingredient-item");
    let quantityInputs = document.getElementsByClassName("ingredient-quantity");
    let unitInputs = document.getElementsByClassName("ingredient-unit");
    let nameInputs = document.getElementsByClassName("ingredient-name");
    let stepItems = document.getElementsByClassName("preparation-item");
    let stepInputs = document.getElementsByClassName("preparation_step");

    // Validate Recipe Name
    if (recipeName === "") {
        alert("Please enter a recipe name.");
        return false;
    }


    // Validate Difficulty
    if (difficulty === "") {
        alert("Please select a difficulty level.");
        return false;
    }

    // Validate Time
    if (time === "" || isNaN(time) || parseFloat(time) <= 0) {
        alert("Please enter a valid positive time for the recipe.");
        return false;
    }

    // Validate Image
    if (image === "") {
        alert("Please upload an image for the recipe.");
        return false;
    }

    // Validate Category
    if (category === " ") {
        alert("Please choose a category.");
        return false;
    }

    // Validate Ingredients


    for (let i = 0; i < ingredientItems.length; i++) {
        let quantityValue = quantityInputs[i].value.trim();
        let unitValue = unitInputs[i].value.trim();
        let nameValue = nameInputs[i].value.trim();

        if (isNaN(quantityValue) || quantityValue <= 0) {
            alert(`Please enter a valid positive number for the quantity in ingredient ${i + 1}.`);
            return false;
        }
        if (unitValue === "") {
            alert(`Please enter a unit for ingredient ${i + 1}.`);
            return false;
        }
        if (nameValue === "") {
            alert(`Please enter a name for ingredient ${i + 1}.`);
            return false;
        }
    }

    // Validate Preparation Steps


    for (let i = 0; i < stepItems.length; i++) {
        let stepValue = stepInputs[i].value.trim();
        if (stepValue === "") {
            alert(`Please describe preparation step ${i + 1}.`);
            return false;
        }
    }

    alert("Recipe submitted successfully!");
    return true;
}



