# https://github.com/pauzon/
# pylint: disable=missing-module-docstring
# pylint: disable=trailing-whitespace

import io

import duckdb
import pandas as pd
import streamlit as st

CSV1 = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV1))

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT *
FROM beverages
CROSS JOIN food_items;
"""

solution_df = duckdb.sql(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        label="What would you like to review?",
        options=("Joins", "GroupBy", "Windows function"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"You selected: {option}")

st.write("""
# SQL SRS
Space repetition System SQL practice
""")

st.header("Entrer votre code : ")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution_df.columns):
        st.write("Some columns are missing")

    try:
        result = result[solution_df.columns]
    except KeyError as e:
        st.write(f"Somme columns are missing : {e}")

    n_line_differences = result.shape[0] - solution_df.shape[0]

    if n_line_differences != 0:
        st.write(f""" result has a {n_line_differences} lines differences 
            with the solution_df """)

    try:
        st.dataframe(result.compare(solution_df))
    except ValueError as e:
        st.write(f"Compare not possible  : {e}")

tab2, tab3 = st.tabs(["Tables", "solution_df"])

with tab2:
    st.write("table : beverages")
    st.dataframe(beverages)
    st.write("table : food_items")
    st.dataframe(food_items)
    st.write("Expected : ")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
