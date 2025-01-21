# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests


# Write directly to the app
st.title("Snoflake Training")
st.write("""Snowflake Training""")



###########################
# Credentials & Data
###########################

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

# Create a DF of the fruit names
my_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_df, use_container_width=True)


# Create a pandas DF of the fruit names
pd_df = my_df.to_pandas()
st.dataframe(data=pd_df, use_container_width=True)
st.stop()



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

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', ingredient,' is ', search_on, '.')


        st.subheader(f" {ingredient} Nutritional Information")    
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    
    time_to_insert = st.button('Submit Order')
    

    if time_to_insert:
        
        # If there are ingredients selected, give option to create an order
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

