# streamlit_app.py

import streamlit as st
import pandas as pd
import Database.dbConnection as dbConnection
import datetime
import plotly.express as px
from pandas.api.types import is_numeric_dtype
def onSelectChange(option):
    # st.write(option)
    global op,current_data_col
    x=run_query(f'SELECT * FROM "BANKING"."{option}"')
    y=run_query(f'SELECT COLUMN_NAME,ORDINAL_POSITION FROM "INFORMATION_SCHEMA"."COLUMNS" where UPPer("TABLE_NAME") LIKE UPPER(\'{option}\')')
    t=[""]*len(y)
    for heading in y:
        t[heading[1]-1]=heading[0]
    current_data_col=t
    print(y)
    op=pd.DataFrame(x,columns=t)
    return op
n=0
def showTable(data : pd.DataFrame):
    global n
    st.write(data.head(n if n!=None else len(data)))

def lineChart(data,x,y):
    if(is_numeric_dtype(data[x]) and y):
        st.line_chart(data,x=x,y=y)
    
    if(is_numeric_dtype(data[y]) and x):
        st.line_chart(data,x=x,y=y)

def barChart(data,x,y):
    if(is_numeric_dtype(data[x]) and y):
        st.bar_chart(data,x=x,y=y)
    
    if(is_numeric_dtype(data[y]) and x):
        st.bar_chart(data,x=x,y=y)
def pie_Chart(data,x,y):
    if(type(data[x][0])==datetime.date or type(data[y][0])==datetime.date):
        return
    fig = px.pie(data, values=y, names=x)
    st.plotly_chart(fig)
run_query=dbConnection.run_query
current_data_col=[]
rows = run_query('SELECT * FROM "BANKING"."DATASETS"')
op=pd.DataFrame()
data=pd.DataFrame(rows)

option1=None
option2=None
col1,col2=st.columns(2)

with col1:
    
    option = st.selectbox(
        'Which Data would you like to view?',data.index,format_func=lambda x:data[1][x])
    onSelectChange(option=data[0][option])
with col2:
    n=st.selectbox('Count',(10,50,100,None),index=0)
    

showTable(op)
c1,c2=st.columns(2)
    
with c1:
    option1 = st.selectbox(
        'X',current_data_col)
with c2:
    option2 = st.selectbox(
        'Y',current_data_col)
values=[0,0]
print(type(op[option1][0])==datetime.date)

if(type(op[option1][0])==datetime.date):
    values = st.slider(
    'Select a range of Date',
    min(op[option1]), min(op[option1]), (min(op[option1]), max(op[option1])))
    print(values)
    op=op[(op[option1]>=values[0]) & (op[option1]<=values[1])]

lineChart(op,option1,option2)
pie_Chart(op,option1,option2)
