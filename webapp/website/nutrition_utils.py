# import requests
# import json
# #to get existing food name from partially inputted food name
# #input string partial name
# #output list of auto completed name
# def get_auto_complete(name):
# 	query={
# 		"app_id":"305d7f9f",
# 		"app_key":"41fbf057040b55dcc3fa2d6a0d6fc818",
# 		"q":name,
# 		"limit":"5"
# 	}
# 	response = requests.get("https://api.edamam.com/auto-complete",params=query)
# 	#print(type(response.json()))
# 	return response.json()

# #to get quantity label for food item
# #e.g. cup, count, liter 
# #input: food name from get_auto_complete
# #output: map containing:
# #	found: boolean, true if name input is found
# #   foodId: foodId as a string
# #   measures: a list of tuple of two elements, where the first element is name for measure, second element is measureURI
# def get_quantity_label(name):
# 	query={
# 		"app_id":"305d7f9f",
# 		"app_key":"41fbf057040b55dcc3fa2d6a0d6fc818",
# 		"ingr":name,
# 	}
# 	response=requests.get("https://api.edamam.com/api/food-database/v2/parser",params=query);
# 	found=len(response.json()["parsed"]) ==1

# 	foodId=response.json()["hints"][0]["food"]["foodId"]

# 	res=[]#(measure name, measure uri)
# 	for i in response.json()["hints"][0]["measures"]:
# 		res.append((i["label"],i["uri"]))

# 	return {"found":found,"foodId":foodId,"measuers":res}


# #return a map containing nutrition for inputted food name with given quantity of given measure
# #input: name: food name of the ingredient
# #measure: measureURI. could be obtained from get_quantity_label method; 
# #quantity: amount of such measurement. i.e. 2 cups, 3 liters
# def get_nutrition(foodId,measure,quantity):
# 	query={
# 		"app_id":"305d7f9f",
# 		"app_key":"41fbf057040b55dcc3fa2d6a0d6fc818",
# 	};

# 	ingredients_input={"ingredients":[
# 		{
# 			"quantity":quantity,
# 			"measureURI":measure,
# 			"foodId":foodId
# 		}
# 	]}
# 	response=requests.post("https://api.edamam.com/api/food-database/v2/nutrients", json=ingredients_input,params=query)
# 	return response.json()
