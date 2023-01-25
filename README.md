# Metis_ENG_2023 - The Fridge Scrounger: A simple recipe recommender web app. 

---
### This is a writeup/README for my project from Metis Data Engineering Module. You can access its Streamlit app Rev.1 via [this link](https://rageofpaju-metis-eng-appfridge-scrounger-project-rev1-1trjwl.streamlit.app/).
---
Repo Table of Contents:
- [App](https://github.com/rageofpaju/Metis_ENG/tree/main/App): Contains the main project materials and MVP
	- Codes and related files for my main project
		- [fridge_scrounger_project_rev1.py](https://github.com/rageofpaju/Metis_ENG/blob/main/App/fridge_scrounger_project_rev1.py): My main code; a .py file for Streamlit deployment
		- df_recipe_topic_labeled_eng_reduced.csv: Recipes dataset with topics assigned; this file is a reduced version of the original file to be used as a showcase example. 
	- '[MVP' folder](https://github.com/rageofpaju/Metis_ENG/tree/main/App/MVP): a folder containing codes and data that I submitted for the MVP
- [Presentation](https://github.com/rageofpaju/Metis_ENG/blob/main/Presentation/): Contains presentation slide 
---



## ABSTRACT
You know there are times when you need to cook some food to feed yourself, you open up your refridgerator and see a bunch of ingredients lying around, but you just can't decide what to make.

I aimed to build a data pipeline, a simple web app, based on a dataset with topics labeled via a previously-built NLP model from my previous project, that suggests you  a possible dish that you can cook out of the ingredients you have.  

In a way, this is an extension of the NLP project, where I have built a topic model for a food.com recipe dataset to label each recipes with according topic. 

## DATA
- Original Source of data 
	- A CSV file of Food.com recipes dataset obtained from Kaggle  (shorturl.at/jzCRY)
	- Some of its columns include name, prep/cook time, ingredients, ratings, calories, nutritions, instructions
	- 550,000 entries

- Dataset Preprocessing
	- The source dataset was cleaned (removal of uneccessary puncuations, removal of null values for relevant columns, dropping unecessary columns) and its number of entries reduced down to about 330,000 total.
	- Then the dataset was run through a NMF topic model that I have built previously on NLP project in order to assign ropics.
	- The preprocessed dataset was stored as CSV file so it can be directly read from the cloud storage

## DESIGN
1. **Data Ingestion**: csv downloaded from kaggle, preprocessing with a NMF-based topic model
2. **Storage**: cloud stroage for the main dataset (~750MB); Github repo for the app (and also a showcase dataset) 
3. **Processing / Writing An App**: Data manipulation in-app. Taking user inputs and creating filters based on them. Suggesting a random recipe under a given criteria. 
5. **Deploying The Recommender App**: [The app](https://rageofpaju-metis-eng-appfridge-scrounger-project-rev1-1trjwl.streamlit.app/) is deplyed on Streamlit, and is connected with Github repo 

## ALGORITHM
- Data Recall: based on a set of documentations provided by Backblaze.
- Preprocessing: NMF-based topic modelling. Assigns a topic that scores the highest fit for each recipe.
- Recommender App: Mainly Pandas data manipulation with user inputs as conditions for Rev1.

## TOOLS
- **Standard Python libraries** such as pandas, numpy, etc for EDA and cleaning the data.
- Some libraries related to unsupervised learning (**sklearn**) for going over the NLP models.
- **Backblaze B2** for majority of remote data storage. **Github Repository** for codes. **Sqlite** for MVP submission. 
- Packaging & Visualization: **Streamlit**

## COMMUNICATION
- Objective and worlflows are summarized in a [presentation slide](https://github.com/rageofpaju/Metis_ENG/blob/main/Presentation/Eng__Final_Presentaion_Ed_Lee.pdf).
- The web app, again, can be accessed via [here](https://rageofpaju-metis-eng-appfridge-scrounger-project-rev1-1trjwl.streamlit.app/). 
<img src="https://github.com/rageofpaju/Metis_ENG/blob/main/app_ex1.png" width="250" height="250"> <img src="https://github.com/rageofpaju/Metis_ENG/blob/main/app_ex2.png" width="250" height="250">
<img src="https://github.com/rageofpaju/Metis_ENG/blob/main/app_ex3.png" width="250" height="250">
