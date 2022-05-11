import requests
import random
from flask import jsonify
import psycopg2
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# heatlhy food list
def get_list(healthy_foods):
    with open("website/healthyfoodlist.txt") as file:
        for line in file:
            healthy_foods.append(line)

# GET USER'S ID
def get_user_id():
    pass

# GET USER'S INFORMATION FROM DATABASE (TO BE IMPLEMENTED)
def get_user_information(user_id):
    user_health = []
    conn = psycopg2.connect(
        host="ec2-52-86-123-180.compute-1.amazonaws.com",
        port="5432",
        database="d2o2cbpkkb06fc",
        user="zunhwbfmndzghr",
        password="97e2dd8a68587ef47ecc4ced5b9137bf7ab6daadada6757c028cf96b81c8ac3b"
    )
    response={}
    keys=["email","alcohol_cocktail","alcohol_free","celery_free","crustacean_free","dairy_free","dash","egg_free","fish_free","fodmap_free","gluten_free","immuno_supportive","keto_friendly","kidney_friendly","kosher","low_potassium","low_sugar","lupine_free","mediterranean","mollusk_free","mustard_free","no_oil_added","paleo","peanut_free","pecatarian","pork_free","red_meat_free","sesame_free","shellfish_free","soy_free","sugar_conscious","sulfite_free","tree_nut_free","vegan","vegetarian","wheat_free"]
    cursor=conn.cursor()
    cursor.execute("SELECT {} from users where email like '{}'".format(",".join(keys),user_id))
    entries=cursor.fetchall()
    conn.commit()
    cursor.close()

    counter = 0
    for i in entries[0]:
        if user_id == i:
            continue

        #Alcohol Cokltail
        if counter == 1:
            if bool(i) == True:
                user_health.append("aclohol-cocktail")
            
        if counter == 2:
            if bool(i) == True:
                user_health.append("alcohol-free")

        if counter == 3:
            if bool(i) == True:
                user_health.append("celery-free") 

        if counter == 4:
            if bool(i) == True:
                user_health.append("crustacean-free")

        if counter == 5:
            if bool(i) == True:
                user_health.append("dairy-free") 

        if counter == 6:
            if bool(i) == True:
                user_health.append("DASH")

        if counter == 7:
            if bool(i) == True:
                user_health.append("DASH") 

        if counter == 8:
            if bool(i) == True:
                user_health.append("egg-free") 

        if counter == 9:
            if bool(i) == True:
                user_health.append("fish-free") 

        if counter == 10:
            if bool(i) == True:
                user_health.append("fodmap-free") 

        if counter == 11:
            if bool(i) == True:
                user_health.append("gluten-free") 

        if counter == 12:
            if bool(i) == True:
                user_health.append("immuni-supportive")

        if counter == 13:
            if bool(i) == True:
                user_health.append("keto-friendly")  

        if counter == 14:
            if bool(i) == True:
                user_health.append("kosher") 

        if counter == 15:
            if bool(i) == True:
                user_health.append("low-potassium") 

        if counter == 16:
            if bool(i) == True:
                user_health.append("low-sugar") 

        if counter == 17:
            if bool(i) == True:
                user_health.append("lupine-free")

        if counter == 18:
            if bool(i) == True:
                user_health.append("Mediterranean") 

        if counter == 19:
            if bool(i) == True:
                user_health.append("mollusk-free") 

        if counter == 20:
            if bool(i) == True:
                user_health.append("mustard-free") 

        if counter == 21:
            if bool(i) == True:
                user_health.append("No-oil-added")   

        if counter == 22:
            if bool(i) == True:
                user_health.append("paleo")

        if counter == 23:
            if bool(i) == True:
                user_health.append("peanut-free")  
    
        if counter == 24:
            if bool(i) == True:
                user_health.append("pecatarian")
    
        if counter == 25:
            if bool(i) == True:
                user_health.append("pork-free")

        if counter == 26:
            if bool(i) == True:
                user_health.append("red-meat-free")

        if counter == 27:
            if bool(i) == True:
                user_health.append("sesame-free")

        if counter == 28:
            if bool(i) == True:
                user_health.append("shellfish-free")

        if counter == 29:
            if bool(i) == True:
                user_health.append("soy-free")   

        if counter == 30:
            if bool(i) == True:
                user_health.append("sugar-conscious")

        if counter == 31:
            if bool(i) == True:
                user_health.append("sulfite-free")

        if counter == 32:
            if bool(i) == True:
                user_health.append("tree-nut-free")   

        if counter == 33:
            if bool(i) == True:
                user_health.append("vegan")
    
        if counter == 34:
            if bool(i) == True:
                user_health.append("vegetarian")

        if counter == 35:
            if bool(i) == True:
                user_health.append("wheat-free")            

        counter += 1

    return user_health



# RANDOM RECIPES
def random_recipes(meal_type,user_health,user_cuisine):
    # Healthy food ingridents list
    healthy_foods = []
    get_list(healthy_foods)

    q = random.choice(healthy_foods)

    # API URL Handling
    query = {
        "app_id": "a42ccba9",
        "app_key": "ed7faabca501242e1578be0f59b949eb",
        "q": q,
        "mealType": meal_type,
        "health": user_health,
        "cuisineType": user_cuisine
    };

    r = requests.get("https://api.edamam.com/api/recipes/v2?type=public&)", params=query)
    access = r.json()
    recipes = access['hits']

    my_response=[]
    # Getting the label, url, image, and ingredient list
    for i in range(len(recipes)):
        recipe = recipes[i]
        label = recipe["recipe"]['label']
        recipe_url = recipe["recipe"]['url']
        recipe_img = recipe["recipe"]['image']
        type_meal = str(recipe["recipe"]['mealType'])
        recipe_calories = str(recipe["recipe"]['calories'])
        recipe_time = str(recipe["recipe"]['totalTime'])
        recipe_cuisine = str(recipe["recipe"]['cuisineType'])
        recipe_ingr = recipe["recipe"]['ingredientLines']

        print(label)
        print("Total Calories: " + recipe_calories)
        print("Total Time To Cook: " + recipe_time)
        print("Cuisine Type: " + recipe_cuisine)
        print("Link to Recipe: " + recipe_url)
        print("Image of Recipe: " + recipe_img)
        print("Meal Type: " + type_meal)
        print("Ingredient List: ")
        for line in recipe_ingr:
            print(line)
        print()
        cur_response={}
        cur_response["label"]=label
        cur_response["Total Calories"]=str(recipe_calories)
        cur_response["Total Time To Cook"]=str(recipe_time)
        cur_response["Cuisine Type"]=str(recipe_cuisine)
        cur_response["Link to Recipe"]=str(recipe_url)
        cur_response["Image of Recipe"]=str(recipe_img)
        cur_response["Meal Type"]=str(type_meal)
        cur_response["Ingredient List"]=list(recipe_ingr)
        my_response.append(cur_response)
    return my_response


# RECIPES API HTTP REQUEST BASED ON SEARCH WORD
def recipe_search(q,meal_type,user_health,user_cuisine):
    # API URL Handling
    query = {
        "app_id": "a42ccba9",
        "app_key": "ed7faabca501242e1578be0f59b949eb",
        "q": q,
        "mealType": meal_type,
        "health": user_health,
        "cuisineType": user_cuisine
    };

    r = requests.get("https://api.edamam.com/api/recipes/v2?type=public&)", params=query)
    access = r.json()
    recipes = access['hits']

    my_response=[]
    # Getting the label, url, image, and ingredient list
    for i in range(len(recipes)):
        recipe = recipes[i]
        label = recipe["recipe"]['label']
        recipe_url = recipe["recipe"]['url']
        recipe_img = recipe["recipe"]['image']
        type_meal = str(recipe["recipe"]['mealType'])
        #recipe_health_labels = str(recipe["recipe"]['healthLabels'])
        recipe_calories = str(recipe["recipe"]['calories'])
        recipe_time = str(recipe["recipe"]['totalTime'])
        recipe_cuisine = str(recipe["recipe"]['cuisineType'])
        recipe_ingr = recipe["recipe"]['ingredientLines']

        print(label)
        print("Total Calories: " + recipe_calories)
        print("Total Time To Cook: " + recipe_time)
        print("Cuisine Type: " + recipe_cuisine)
        print("Link to Recipe: " + recipe_url)
        print("Image of Recipe: " + recipe_img)
        #print("Labels: " + recipe_health_labels)
        print("Meal Type: " + type_meal)
        print("Ingredient List: ")
        for line in recipe_ingr:
            print(line)
        print()
        cur_response={}
        cur_response["label"]=label
        cur_response["Total Calories"]=str(recipe_calories)
        cur_response["Total Time To Cook"]=str(recipe_time)
        cur_response["Cuisine Type"]=str(recipe_cuisine)
        cur_response["Link to Recipe"]=str(recipe_url)
        cur_response["Image of Recipe"]=str(recipe_img)
        cur_response["Meal Type"]=str(type_meal)
        cur_response["Ingredient List"]=list(recipe_ingr)
        my_response.append(cur_response)
    return my_response


# Main File Testing
#q = input("Search food to get recipe (Example: Chicken pasta):  ")
#meal_type = []
#user_health = []
#user_cuisine = []

#recipe_search(q,meal_type,user_health,user_cuisine)
#random_recipes(meal_type,user_health,user_cuisine)
#get_user_information(7)