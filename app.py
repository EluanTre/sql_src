# https://github.com/pauzon/
# pylint: disable=missing-module-docstring
# pylint: disable=trailing-whitespace
# pylint: disable=exec-used
# pylint: disable=consider-using-with

import os
from datetime import date, timedelta
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

current_path = Path()
data_dir_path = current_path / "data"
data_dir_path.mkdir(exist_ok=True)

if "exercices_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py", encoding="utf-8").read())

conn = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str, result_df: pd.DataFrame) -> None:
    """
    Checks a user's SQL query result against an expected solution DataFrame.

    The function executes the provided SQL query, displays its result, and
    compares the resulting DataFrame with the expected solution. It checks
    for differences in the number of columns, missing columns, number of rows,
    and cell values.

    Warnings are displayed through Streamlit when discrepancies are detected.
    A DataFrame containing the differences between the query result and the
    expected solution is also displayed when possible.

    Args:
        user_query: SQL query provided by the user. The query is executed
            using the database connection.
        result_df: Expected result as a pandas DataFrame. Its columns and
            values are used as the reference for comparison.

    Returns:
        None
    """

    result = conn.execute(user_query).df()
    st.dataframe(result)

    if len(result.columns) != len(result_df.columns):
        st.warning("Some columns are missing")

    try:
        result = result[result_df.columns]
    except KeyError as e:
        st.warning(f"Somme columns are missing : {e}")

    n_line_differences = result.shape[0] - result_df.shape[0]

    if n_line_differences != 0:
        st.warning(f""" result has a {n_line_differences} lines differences 
            with the result_df """)

    try:
        st.dataframe(result.compare(result_df))

        if result.compare(result_df).shape == (0, 0):
            st.success("Correct !")
    except ValueError as e:
        st.error(f"{e}")


with st.sidebar:
    available_themes_df = conn.execute("""
        SELECT DISTINCT theme
        FROM memory_state_db;
        """).df()

    theme = st.selectbox(
        label="What would you like to review?",
        options=available_themes_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )

    if theme:
        st.write(f"You selected: {theme}")
        SELECT_EXERCISE_QUERY = f"""
            SELECT * 
            FROM memory_state_db
            WHERE theme LIKE '{theme}';
            """
    else:
        SELECT_EXERCISE_QUERY = """
            SELECT * 
            FROM memory_state_db;
            """

    exercise = (
        conn.execute(SELECT_EXERCISE_QUERY)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )

    st.write(exercise)
    exercise_name = exercise.loc[0, "exercice_name"]
    with open(f"answer/{exercise_name}.sql", "r", encoding="utf8") as f:
        answer = f.read()

    solution_df = conn.execute(answer).df()

st.write("""
# SQL SRS
Space repetition System SQL practice
""")

st.header("Entrer votre code : ")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    check_users_solution(query, solution_df)

for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        conn.execute(f"""
            UPDATE memory_state_db SET last_reviewed = '{next_review}'
            WHERE exercice_name = '{exercise_name}'
            """)
        st.rerun()

if st.button("Reset"):
    conn.execute("UPDATE memory_state_db SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "solution_df"])

with tab2:

    exercice_tables = exercise.loc[0, "tables"]
    for table in exercice_tables:
        st.write(f"Table : {table}")
        df_table = conn.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.code(answer, language="sql")
