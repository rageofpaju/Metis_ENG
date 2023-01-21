import numpy as np
import pandas as pd
import matplotlib as plt
import sklearn
import streamlit as st
from sqlalchemy import create_engine

#import gcsfs
#from google.oauth2 import service_account
#from google.cloud import storage
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)
#client = storage.Client(credentials=credentials)
# Imports the Google Cloud client library
#from google.cloud import storage
# Instantiates a client
#storage_client = storage.Client()
# The name for the new bucket
#bucket_name = "bucket_lhs"
# Creates the new bucket
#bucket = storage_client.create_bucket(bucket_name)
#print(f"Bucket {bucket.name} created.")

pd.set_option('display.max_columns', None)

st.write(
'''
# MVP Rev.01
## Recipes Recommender, based on food types and ingredients

''')

#df = pd.read_csv('df_recipe_topic_labeled.csv')
#df = pd.read_csv('gs://bucket_lhs/eng_db/df_recipe_topic_labeled.csv')
#data = data.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'})
#df = pd.read_csv('C:/Git Storage/Engineering/df_recipe_topic_labeled_mvp.csv')
engine_recipes = create_engine('sqlite:///c:/Git Storage/Engineering//mvp_recipe.db').connect()
df = pd.read_sql_table('df_recipe_topic_labeled_mvp', engine_recipes)

df.head(15)

#st.dataframe(data)
#st.table(data)

#topic_labels = ['Stew', 'Dessert', 'Entree', 'Pasta&Casserole', 'Baked']

st.write(
'''
## What kind of food do you want to cook?
''')
choose_topic = st.selectbox(
'Choose a category',
('Stew', 'Dessert', 'Entree', 'Pasta&Casserole','Baked'))
st.write('You have selected:', choose_topic)
topic_filtered = df.loc[df['Topic'] == choose_topic]
# RecipeIngredientQuantities, RecipeIngredientParts 	ReviewCount	FatContent	SaturatedFatContent	CholesterolContent	SodiumContent	CarbohydrateContent	FiberContent	SugarContent	ProteinContent	RecipeServings	RecipeYield	RecipeInstructions	Topic
#TopicTotalTime, Description, AggregatedRating, 
#topic_filtered

st.write(
'''
## Which ingredients do you have available / want to use?
Type in the ingredients in lowercase.  You can leave these fields empty.
''')
ingred1 = st.text_input("Ingredient Available 1")
ingred2 = st.text_input("Ingredient Available 2")
ingred3 = st.text_input("Ingredient Available 3")
#https://stackoverflow.com/questions/37011734/pandas-dataframe-str-contains-and-operation
base = r'^{}'
expr = '(?=.*{})'
lookup_ingred = [ingred1, ingred2, ingred3]  # example
lookup_tesrgets = base.format(''.join(expr.format(w) for w in lookup_ingred))

filter_ingredients = topic_filtered[topic_filtered['RecipeIngredientParts'].str.contains(lookup_tesrgets, regex = True)]
filter_ingredients.reset_index(drop=True)

if filter_ingredients.empty == True:
    st.write(
    '''
    # ***No matching recipes found with the ingredients you entered!***
    ''')

st.write(
'''
## How much calories do you want? 
''')
calories_slider = st.slider('Calorie Range', float(filter_ingredients['Calories'].min()), float(filter_ingredients['Calories'].max()), (0., float(filter_ingredients['Calories'].max())))

if st.button('I don\'t care about the calories!'):
    filter_calories = filter_ingredients
else:
    filter_calories = filter_ingredients[(filter_ingredients['Calories'] <= calories_slider[1]) & (filter_ingredients['Calories'] >= calories_slider[0])]



if filter_calories.empty == True:
    st.write(
    '''
    # ***No matching recipes found with the calories you entered!***
    ''')
else:
    st.write(
    '''
    ## Here is one food and how to make it.
    ''')
    food_suggestion = filter_calories[['Name', 'RecipeInstructions','RecipeIngredientParts','Calories']].sample(1)
    food_suggestion.reset_index(drop=True, inplace=True)

    st.write(
    '''
    * Dish Name:
    ''')
    food_suggestion['Name'][0]
    st.write(
    '''
    * Calories:
    ''')
    food_suggestion['Calories'][0]
    st.write(
    '''
    * Ingredients:
    ''')
    food_suggestion['RecipeIngredientParts'][0]
    st.write(
    '''
    * Recipe:
    ''')
    food_suggestion['RecipeInstructions'][0]
    
st.button('Reroll')






#'CookTime', 'PrepTime', 'RecipeServings', 'RecipeYield', 'RecipeInstructions', 'Calories']
#price_input = st.slider('House Price Filter', int(data['PRICE'].min()), int(data['PRICE'].max()), 500000 )