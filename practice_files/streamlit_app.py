"""
Streamlit Housing App Demo
    
Make sure to install Streamlit with `pip install streamlit`.

Run `streamlit hello` to get started!

To run this app:

1. cd into this directory
2. Run `streamlit run streamlit_app.py`
"""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# We begin with Parts 3, 6, and 7, but uncomment the code in each of the other parts and save to see how the Streamlit application updates in your browser.


### PART 1 - Agenda

st.write('''
# Welcome To Streamlit!
In this Streamlit app we will cover:

- Markdown
- Importing data
- Displaying dataframes
- Graphing
- Interactivity with buttons
- Mapping
- Making predictions with user input
''')


## PART 2 - Markdown Syntax

st.write(
'''
## Markdown Syntax
You can use Markdown syntax to style your text. For example,

# Main Title
## Subtitle
### Header

**Bold Text**

*Italics*

Ordered List

1. Apples
2. Oranges
3. Bananas

[This is a link!](https://docs.streamlit.io/en/stable/getting_started.html)

'''
)


# PART 3 - Seattle House Prices Table

st.write(
'''
## Seattle House Prices
We can import data into our Streamlit app using pandas `read_csv` then display the resulting dataframe with `st.dataframe()`.

''')

data = pd.read_csv('practice_files/SeattleHomePrices.csv')
data = data.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'})
st.dataframe(data)


# PART 4 - Graphing and Buttons

st.write(
'''
#### Graphing and Buttons
#Let's graph some of our data with matplotlib. We can also add buttons to add interactivity to our app.
#'''
)

fig, ax = plt.subplots()

ax.hist(data['PRICE'])
ax.set_title('Distribution of House Prices in $100,000s')

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
     st.pyplot(fig)


# PART 5 - Mapping and Filtering Data

st.write(
'''
### Mapping and Filtering Data
#We can also use Streamlit's built in mapping functionality.
#Furthermore, we can use a slider to filter for houses within a particular price range.
#'''
)

price_input = st.slider('House Price Filter', int(data['PRICE'].min()), int(data['PRICE'].max()), 500000 )

price_filter = data['PRICE'] < price_input
st.map(data.loc[price_filter, ['lat', 'lon']])


# PART 6 - Linear Regression Model

st.write(
'''
## Train a Linear Regression Model
Now let's create a model to predict a house's price from its square footage and number of bedrooms.
'''
) 

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

clean_data = data.dropna(subset=['PRICE', 'SQUARE FEET', 'BEDS'])

X = clean_data[['SQUARE FEET', 'BEDS']]
y = clean_data['PRICE']

X_train, X_test, y_train, y_test = train_test_split(X, y)

## Warning: Using the above code, the R^2 value will continue changing in the app. Remember this file is run upon every update! Set the random_state if you want consistent R^2 results.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

lr = LinearRegression()
lr.fit(X_train, y_train)

st.write(f'Test R²: {lr.score(X_test, y_test):.3f}')


# PART 7 - Predictions from User Input

st.write(
'''
## Model Predictions
And finally, we can make predictions with our trained model from user input.
'''
)

sqft = st.number_input('Square Footage of House', value=2000)
beds = st.number_input('Number of Bedrooms', value=3)

input_data = pd.DataFrame({'sqft': [sqft], 'beds': [beds]})
pred = lr.predict(input_data)[0]

st.write(
f'Predicted Sales Price of House: ${int(pred):,}'
)
