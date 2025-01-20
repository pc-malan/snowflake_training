# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom smoothie.""")



###########################
# Credentials & Data
###########################

# Get the current credentials
session = get_active_session()

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

    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    

    if time_to_insert:
        
        # If there are ingredients selected, give option to create an order
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
