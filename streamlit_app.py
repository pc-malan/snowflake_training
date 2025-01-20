# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests


# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom smoothie.""")



###########################
# Credentials & Data
###########################

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

# Create a DF of the fruit names
my_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))



###########################
# Front-End
###########################


# Name
name_on_order = st.text_input('Name on Smoothie')



# Ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_df
    , max_selections=6
)



# Submission
if ingredients_list:
    ingredients_string = ''

    for ingredient in ingredients_list:
        ingredients_string+= ingredient + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    
    time_to_insert = st.button('Submit Order')
    

    if time_to_insert:
        
        # If there are ingredients selected, give option to create an order
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text()


sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)