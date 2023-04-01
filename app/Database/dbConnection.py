
import streamlit as st
import snowflake.connector
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["banking"], client_session_keep_alive=True
    )
@st.cache_data
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

conn = init_connection()