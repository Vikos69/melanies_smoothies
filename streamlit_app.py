# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!.
    """
)

## 🥋 Add a Name Box for Smoothie Orders
title = st.text_input("Name on Smoothie:")
st.write("the name on you Smoothie will be:", title)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#🥋 Add a Multiselect  ESTABA EN LINEA 18
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    #🥋 Researching Limiting Entries on Streamlit Multiselects
    , max_selections=5
)

## 🥋 Cleaning Up Empty Brackets
if ingredients_list:
    ## 🥋 Display the LIST ESTABA LINEA 25
    ## 🥋 Improve the String Output SE ELIMINAN EN PASO 5
    ##st.write(ingredients_list)
    ##st.text(ingredients_list)

    ## 🥋 Create the INGREDIENTS_STRING Variable 
    ingredients_string = ''
    name_on_order = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    name_on_order = title

    ## 🥋 Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    st.write(my_insert_stmt)
    # st.stop()
    
    # 🥋 Add a Submit Button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + name_on_order, icon="✅")

    # 🥋 Insert the Order into Snowflake
    # if ingredients_string:
    #    session.sql(my_insert_stmt).collect()
    #    st.success('Your Smoothie is ordered!', icon="✅")

## 🥋 Remove the SelectBox ESTABA EN LINEA 14
##option = st.selectbox(
##    "What is your favorite fruits?",
##    ("Banana", "Strawberries", "Peaches"),
##)
##st.write("Your favorite fruit is:", option)
