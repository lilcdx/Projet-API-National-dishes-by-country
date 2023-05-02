# installer api : pip install python-marmiton==0.4.2

import json
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt
from marmiton import Marmiton, RecipeNotFound

import requests



DOWNLOAD_DELAY = 3
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

def request(recette) :
  """ recherche de la recette dans l'api"""
  url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"

  querystring = {"query": recette}

  headers = {
    "X-RapidAPI-Key": "83a6963234msh0bbe7695ea2c9bcp15db06jsn57c4bd6f2a23",
    "X-RapidAPI-Host": "recipe-by-api-ninjas.p.rapidapi.com"
  }

  response = requests.get(url, headers=headers, params=querystring)
  return response.json()


def csvToDic(file) :
    """ transforme le fichier csv en liste de dictionnaires"""
    allDishes = []
    f = open(file, 'r')
    cr = csv.DictReader(f, delimiter=";") # lecture du csv comme un tableau
    for row in cr :
      if row['country'] != '' :
        sortDishes(row, allDishes) #ajout de la ligne à la liste allDishes
    return allDishes

def sortDishes(row, allDishes) :
  """ajoute la ligne du fichier csv mise en parametre a la liste de dictionnaire allDishes"""
  exist = False #booleen qui permet de savoir si le pays existe déjà dans la liste

  for e in allDishes : #parcours de la liste

    if row["country"] == e["country"] : # le pays est déjà dans le tableau (il peut y avoir plusieurs plats nationaux)
      e["dishes"].append(row["dish"]) #ajout du plat au dictionnaire qui correspond au pays
      exist = True
      break
  # pays n'existe pas dans la liste
  if exist == False :
    dic = {'country' : row["country"], 'dishes' : [row["dish"]]} #creation du dictionnaire associé au pays
    allDishes.append(dic)

def getRecipe(allDishes) :
  """ permet d'attribuer à chaque pays une recette principale"""
  for country in allDishes : #parcours des pays
    mainRecipe = ""
    maxlength = 0
    
    for dish in country['dishes'] :
      res = request(dish)
      print(res)
      if res != [] : #si on obtient une réponse à la requête
        if len(res) > maxlength : #on sélectionne le plat qui a le plus de résultats à la requête
          mainRecipe = request(dish)[0]
          mainRecipe['instructions'] == mainRecipe['instructions']
          maxlength = len(res)

    country["recipe"] = mainRecipe #on attribue la recette au pays
    print(country)

def writeJson(listCountry, path) :
  """ ecriture de la liste de dictionnaire dans un json"""
  with open(path,"w") as f:
            json.dump(listCountry,f, indent=3)

##### PREMIERS ESSAIS NON CONLUANTS #####

#### Utilisation de l'API Marmiton ####
#### Changement car informations trouvées uniquement en anglais et echec de la fonction de traduction ####
#### Choix de l'autre API car résultats plus précis

# def searchRecipe(dish) :
#   query_options = {
#     "aqt": dish,  # Query keywords - separated by a white space
#   }

#   query_result = Marmiton.search(query_options)
#   if len(query_result)>0 :
#     return query_result
#   else :
#     print("No match found for "+ dish)

# def sortRecipes(recipesList) :
#   bestRecipe = recipesList[0]
#   if len(recipesList) >1 :
#     for recipe in recipesList :
#       if recipe['rate'] > bestRecipe['rate'] :
#         bestRecipe = recipe
#       # elif recipe['rate'] == bestRecipe['rate'] :
#       #   if recipe['nb_comments'] > bestRecipe['nb_comments'] :
#       #     bestRecipe = recipe
#   return bestRecipe

#### TRADUCTION ####
#### Différents tests avec google traduction, deepl
#### Problème : pas réussi à envoyer du texte dans la zone de texte
#### Essais en cherchant l'élément par plusieurs moyens + essais d'autres éléments

# def traduction(recette, driver) :
#   driver.get("https://www.deepl.com/fr/translator")
#   time.sleep(4)
#   WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME,"lmt__textarea"))
#   )
#   textInput = driver.find_element((By.CLASS_NAME,"lmt__textarea"))
#   time.sleep(2)
#   textInput.click()
#   textInput.clear()
#   print(recette)
#   textInput.sendKeys("test")
#   time.sleep(3)

if __name__ == "__main__" :

  t = csvToDic("Ressources/foodculture_dishes_rev2.csv")
  getRecipe(t)
  writeJson(t, "Ressources/national_dishes_recipes.json")
  


