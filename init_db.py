import io
import duckdb
import pandas as pd

conn = duckdb.connect(database='data/exercices_sql_tables.duckdb', read_only=False)

# -------------------------------------------------------------------------
# EXERCICES LIST
# -------------------------------------------------------------------------

data = {
    "theme": ["cross_join", "window_functions"],
    "exercice_name": ["beverages_and_food", "simple_window"],
    "tables": [["beverages_db", "food_items_db"], "simple_window"],
    "last_reviewed": ['1970-01-01', '1970-01-01'],
}
memory_state_df = pd.DataFrame(data)
conn.execute("""
             CREATE TABLE IF NOT EXISTS memory_state_db AS 
             SELECT * 
             FROM memory_state_df;
             """)

# -------------------------------------------------------------------------
# CROSS JOIN EXERCICES
# -------------------------------------------------------------------------

CSV1 = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages_df = pd.read_csv(io.StringIO(CSV1))
conn.execute("""
             CREATE TABLE IF NOT EXISTS beverages_db AS 
             SELECT * 
             FROM beverages_df;
             """)

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items_df = pd.read_csv(io.StringIO(CSV2))
conn.execute("""
             CREATE TABLE IF NOT EXISTS food_items_db AS 
             SELECT * 
             FROM food_items_df;
             """)
