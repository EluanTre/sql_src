import duckdb
import pandas as pd
import streamlit as st

st.write("""
# SQL SRS
Space repetition System SQL practice
""")

option = st.selectbox(
    label="What would you like to review?",
    options=("Joins", "GroupBy", "Windows function"),
    index=None,
    placeholder="Select a theme...",
)

st.write(f"You selected: {option}")

data = {'a': [1, 2, 3], 'b': [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(['Cat', 'Dog', 'Owl'])

with tab1:
    try:
        query = st.text_area(label="Entrez votre input")
        st.write(f"Vous avez entrer la requête SQL suivante : {query}")
        st.dataframe(duckdb.sql(query).df())
    except AttributeError:
        pass

with tab2:
    st.header('A dog')
    st.image('https://static.streamlit.io/examples/dog.jpg', width=200)

with tab3:
    st.header('An owl')
    st.image('https://static.streamlit.io/examples/owl.jpg', width=200)