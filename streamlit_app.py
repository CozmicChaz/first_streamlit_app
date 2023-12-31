import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),default=['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]



# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+"kiwi")
# streamlit.text(fruityvice_response.json())

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return  fruityvice_normailzed

streamlit.header('Fruit Info') 
try:
  fruit_choice=streamlit.text_input("Please select fruit to get more info")
  if not fruit_choice:
      streamlit.error("what fruit?")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.err()

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#addFruit=streamlit.multiselect("Pick additional fruit:", list(my_fruit_list.index))
addFruit=streamlit.text_input("Please pick fruit to add")
streamlit.write('The user entered ', addFruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
