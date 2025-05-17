let lang = {
  ar: {
    EditProfile: "تعديل الملف الشخصي",
    userName: "اسم المستخدم",
    SavedRecipes: "الوصفات المحفوظة",
    MyRecipeList: "قائمة وصفاتي",
    FavoriteRecipes: "الوصفات المفضلة", 
    AddARecipe: "إضافة وصفة",           
    MyBestRecipes: "أفضل وصفاتي"
  },
  en: {
    EditProfile: "Edit Profile",
    userName: "Username",
    SavedRecipes: "Saved Recipes",
    FavoriteRecipes: "Favorite Recipes",
    AddARecipe: "Add a Recipe",
    MyRecipeList: "Recipe List",
    MyBestRecipes: "My Best Recipes"
  }
}
let selector = document.getElementById("language-selector");
selector.onchange = updateLanguage;

function updateLanguage() {

    let language = selector.options[selector.selectedIndex].value;
    let nodes = document.querySelectorAll("[data-lang]");
    // kolchi li 3ndk f html khass ykoun 3ndu data-lang
    // w f javascript khass ykoun 3ndu data-lang

    let i = nodes.length;// 3ndk l3adad dyal les elements li 3ndk f html
    while (i--) //min nkamal nmchi limba3dha 
    {
         let key = nodes[i].getAttribute("data-lang");// 3ndk f html data-lang="username"....ya3ni kolchi les valeurs dylha
      nodes[i].innerHTML = lang[language][key];// nduro mise à jour l valeur dyal les elements li 3ndk f html w key howa lora kifach
        // 3ndk f html data-lang="username" w lang=ar w key= username rayradha b arbiya

    }
}
//dark mode
var icon = document.getElementById("icon");//SELECTIONEN LES ELEMENTS
icon.onclick = function() {//AJOUTER UN EVENMENE CLICK
    document.body.classList.toggle("dark-theme");//MODDIFICATION DE THEME DE BADY
    if (document.body.classList.contains("dark-theme")) {
        icon.src = "img/sun.png";
    } else {
        icon.src = "img/moon.png";
    }
   
}

