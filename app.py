# https://github.com/pauzon/
# pylint: disable=missing-module-docstring
# pylint: disable=trailing-whitespace

import duckdb
import streamlit as st

conn = duckdb.connect(database='data/exercices_sql_tables.duckdb', read_only=False)

# ANSWER_STR = """
# SELECT *
# FROM beverages
# CROSS JOIN food_items;
# """

# solution_df = duckdb.sql(ANSWER_STR).df()

with st.sidebar:
    theme = st.selectbox(
        label="What would you like to review?",
        options=("cross_join", "groupby", "Windows function"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"You selected: {theme}")
    
    exercise = conn.execute(
        f"""
        SELECT * 
        FROM memory_state
        WHERE theme LIKE '{theme}';
        """).df()
    
    st.write(exercise)

st.write("""
# SQL SRS
Space repetition System SQL practice
""")

st.header("Entrer votre code : ")
query = st.text_area(label="votre code SQL ici", key="user_input")

# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)

#     if len(result.columns) != len(solution_df.columns):
#         st.write("Some columns are missing")

#     try:
#         result = result[solution_df.columns]
#     except KeyError as e:
#         st.write(f"Somme columns are missing : {e}")

#     n_line_differences = result.shape[0] - solution_df.shape[0]

#     if n_line_differences != 0:
#         st.write(f""" result has a {n_line_differences} lines differences 
#             with the solution_df """)

#     try:
#         st.dataframe(result.compare(solution_df))
#     except ValueError as e:
#         st.write(f"Compare not possible  : {e}")

# tab2, tab3 = st.tabs(["Tables", "solution_df"])

# with tab2:
#     st.write("table : beverages")
#     st.dataframe(beverages)
#     st.write("table : food_items")
#     st.dataframe(food_items)
#     st.write("Expected : ")
#     st.dataframe(solution_df)

# with tab3:
#     st.write(ANSWER_STR)
