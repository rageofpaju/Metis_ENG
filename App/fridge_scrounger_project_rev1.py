import numpy as np
import pandas as pd
#import matplotlib as plt
#import sklearn
import streamlit as st
#import sqlite3

#Modules required to import data from cloud
import boto3  # REQUIRED! - Details here: https://pypi.org/project/boto3/
from botocore.exceptions import ClientError
from botocore.config import Config
from dotenv import load_dotenv  # Project Must install Python Package:  python-dotenv
import os
import sys

# Uncomment below for using a cloud storage
#def list_object_keys(bucket, b2):
#    try:
#        response = b2.Bucket(bucket).objects.all()
#        
#        return_list = []               # create empty list
#        for object in response:        # iterate over response
#            return_list.append(object.key) # for each item in response append object.key to list
#        return return_list             # return list of keys from response
#
#    except ClientError as ce:
#        print('error', ce)
#
#
# List browsable URLs of the objects in the specified bucket - Useful for *PUBLIC* buckets
#def list_objects_browsable_url(bucket, endpoint, b2):
#    try:
#        bucket_object_keys = list_object_keys(bucket, b2)
#
#        return_list = []                # create empty list
#        for key in bucket_object_keys:  # iterate bucket_objects
#            url = "%s/%s/%s" % (endpoint, bucket, key) # format and concatenate strings as valid url
#            return_list.append(url)     # for each item in bucket_objects append value of 'url' to list
#        return return_list              # return list of keys from response
#
#   except ClientError as ce:
#       print('error', ce)
#
#     
#b2 = boto3.resource(service_name='s3', 
#                    endpoint_url=st.secrets['ENDPOINT_URL'],                # Backblaze endpoint
#                    aws_access_key_id=st.secrets['credentials']['aws_access_key_id'],              # Backblaze keyID
#                    aws_secret_access_key=st.secrets['credentials']['aws_secret_access_key'], # Backblaze applicationKey
#                    config = Config(signature_version='s3v4',
#                                   ))
#b2 = boto3.resource(service_name='s3',
#                    endpoint_url=st.secrets['ENDPOINT_URL'],                # Backblaze endpoint
#                    config = Config(signature_version='s3v4',\
#                                   ))
#obj_keys = list_object_keys(st.secrets['BUCKET_NAME'], b2)
#obj_url = list_objects_browsable_url(st.secrets['BUCKET_NAME'], st.secrets['ENDPOINT_URL'], b2)
#
#st.write(obj_keys)
#st.write(obj_url)
#data_url = obj_url[0]


pd.set_option('display.max_columns', None)

#https://discuss.streamlit.io/t/how-to-add-extra-lines-space/2220/5
_, col2, _ = st.columns([1, 5, 1])
with col2:
    st.write('#### Can\'t decide what to cook?')
    st.write('''
    # The Fridge Scrounger
    ## :bacon: :avocado: :baguette_bread: :thinking_face: :arrow_right: :sandwich::kissing_smiling_eyes:
    by Ed Lee (Metis_DSML_Eng 2023)
    ''')

# For testing
#df = pd.read_csv('C:/Git Storage/Engineering/df_recipe_topic_labeled_eng_reduced.csv')

# For showcase (github)
df = pd.read_csv('/app/metis_eng/App/df_recipe_topic_labeled_eng_reduced.csv')

# For real thing (backblaze)
#df = pd.read_csv('https://s3.us-west-004.backblazeb2.com/metis-eng-edlee/df_recipe_topic_labeled_mvp_reduced.csv')
#df = pd.read_csv(data_url)



# Input ingredients
st.text("")
st.text("")
st.write(
'''
## Step 1. Which ingredients do you have? \n ##### - Type in up to four major ingredients you **WILL** use.  
- NOTE: The app will search for the recipes that use **ALL** the ingredients you entered.
- You can leave these fields empty if you want.
''')

ingred1 = st.text_input("Ingredient Available 1", placeholder="e.g., chicken, onion, apple, etc...")
ingred2 = st.text_input("Ingredient Available 2", placeholder="e.g., chicken, onion, apple, etc...")
ingred3 = st.text_input("Ingredient Available 3", placeholder="e.g., chicken, onion, apple, etc...")
ingred4 = st.text_input("Ingredient Available 4", placeholder="e.g., chicken, onion, apple, etc...")

#searching for str: https://stackoverflow.com/questions/37011734/pandas-dataframe-str-contains-and-operation
base = r'^{}'
expr = '(?=.* {})' # Adding a space in front of {} is a primitive way to search for exact words
lookup_ingred = [ingred1.lower(), ingred2.lower(), ingred3.lower(), ingred4.lower()]  # example
lookup_tesrgets = base.format(''.join(expr.format(w) for w in lookup_ingred))
#st.write(lookup_tesrgets)
filter_ingredients = df[df['RecipeIngredientParts'].str.contains(lookup_tesrgets, regex = True)]
#st.write(filter_ingredients)

ingredient_flag=0 
if filter_ingredients.empty == True:
    st.write(
    '''
    # ***None of the recipes in the DB uses the ingredient(s) you entered!*** \n ## Please choose a different ingredient(s).
    ''')
    pass
else:
    ingredient_flag=1



# Choosing a Topic
topic_flag = 0
if ingredient_flag==1:
    st.text("")
    st.text("")
    st.write(
    '''
    ## Step 2. What kind of food do you want to make? \n ##### - Think of a loose category.
    ''')
    choose_topic = st.selectbox(
    'Choose a category from the dropbox below:',
     ('Any Category Is Fine', 'Soup & Stew', 'Dessert', 'Chicken', 'Cool Beverages', 'Meat Dish', 'Breads', 'Sides', 'Pasta', 'Roasts', 'Sauces', 'Deli'))
    st.write('### :knife_fork_plate: You have selected:', choose_topic)
    
    if choose_topic=='Any Category Is Fine':
        topic_filtered = df.copy()
    else:
        topic_filtered = df.loc[df['Topic'] == choose_topic]
        # RecipeIngredientQuantities, RecipeIngredientParts 	ReviewCount	FatContent	SaturatedFatContent	CholesterolContent	SodiumContent	CarbohydrateContent	FiberContent	SugarContent	ProteinContent	RecipeServings	RecipeYield	RecipeInstructions	Topic
        #TopicTotalTime, Description, AggregatedRating, 
        #topic_filtered

    st.text("")
    st.text("")
    filter_ingredients = topic_filtered[topic_filtered['RecipeIngredientParts'].str.contains(lookup_tesrgets, regex = True)]
    filter_ingredients.reset_index(drop=True)
    if filter_ingredients.empty == True:
        st.write(
        '''
        # ***No matching recipes found with the ingredient(s) you entered!*** \n ## Please choose a different ingredient(s).
        ''')
        pass
    else:    
        topic_flag = 1
else:
    pass



# Set Cook Time
time_flag = 0
if topic_flag==1:
    st.write(
    '''
    ## Step 3. Are you in a hurry? 
    ''')

    time_slider = st.select_slider('Choose Cook Time',
        options=['NOW!!! (<30min)', 'quick (<1hr)', 'in a couple of hours (<2hrs)', 'eventually'])
    st.write('### :stopwatch: I want it...',time_slider)

    if time_slider=='in a couple of hours (<2hrs)':
        filter_time = filter_ingredients[filter_ingredients['TotalTimeHrs'] <= float(2.0)]
    elif time_slider=='quick (<1hr)':
        filter_time = filter_ingredients[filter_ingredients['TotalTimeHrs'] <= float(1.0)]
    elif time_slider=='NOW!!! (<30min)':
        filter_time = filter_ingredients[filter_ingredients['TotalTimeHrs'] <= float(0.5)]
    elif time_slider=='eventually':
        filter_time = filter_ingredients
        
    if filter_time.empty == True:
        st.write(
        '''
        # ***No matching recipes found with the cook time you entered!***.
        ''')
        pass
    else:    
        time_flag = 1
else:
    pass



# Set calories
calories_flag=0
if time_flag==1:
    st.text("")
    st.text("")
    st.write(
    '''
    ## (Optional) Step 4. How much calories do you want? 
    ''')
    calories_slider = st.slider('Set Calorie Range', float(filter_time['Calories'].min()), float(filter_time['Calories'].max()), (0., float(filter_time['Calories'].max())))
    calories_flag = 1

    if st.button('I don\'t care about the calories!'):
        filter_calories = filter_time
        calories_flag = 1
    else:
        filter_calories = filter_time[(filter_time['Calories'] <= calories_slider[1]) & (filter_time['Calories'] >= calories_slider[0])]
else:
    pass



#if filter_calories.empty == True:
if calories_flag == 0:
    pass
elif filter_calories.empty == True:
    st.write(
    '''
    # ***No matching recipes found with the calories you entered!***
    ''')
    pass
else:
    st.text("")
    st.text("")
    st.write(
    '''
    # :cook: Here's a recipe for you :cook:
    ''')
    #food_suggestion = filter_calories[['Name', 'RecipeInstructions','RecipeIngredientParts','Calories']].sample(1)
    food_suggestion = filter_calories.sample(1)
    food_suggestion.reset_index(drop=True, inplace=True)
    #st.table(food_suggestion)
    
    dish_name = food_suggestion['Name'][0]
    st.write(
    '''
    #### - Dish Name:''', dish_name,'')
    #food_suggestion['Name'][0]

    total_time_hrs = food_suggestion['TotalTimeHrs'][0]
    st.write('* Total Cook Time:', total_time_hrs, 'hours')

    total_calories = food_suggestion['Calories'][0]
    st.write('* Calories:', total_calories, 'kcals')

    total_servings = food_suggestion['RecipeServings'][0]
    st.write('* The recipe makes', total_servings, 'servings')

    st.write(
    '''
    * Ingredients:
    ''')
    food_suggestion['RecipeIngredientParts'][0]
    st.write(
    '''
    * Ingredient Quantities:
    ''')
    food_suggestion['RecipeIngredientQuantities'][0]

    st.write(
    '''
    * Recipe:
    ''')
    food_suggestion['RecipeInstructions'][0]
    
    st.button('Give me something else!')






#'CookTime', 'PrepTime', 'RecipeServings', 'RecipeYield', 'RecipeInstructions', 'Calories']
