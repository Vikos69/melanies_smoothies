# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!.
    """
)

title = st.text_input("Name on Smoothie:")
st.write("the name on you Smoothie will be:", title)

cnx = st.connection("snowflake")
session = cnx.session()

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:

    ingredients_string = ''
    name_on_order = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    name_on_order = title

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + name_on_order, icon="✅")

##    ("Banana", "Strawberries", "Peaches"),
##)
##st.write("Your favorite fruit is:", option)
