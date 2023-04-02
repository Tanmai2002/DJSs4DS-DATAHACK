import pandas as pd
import numpy as np
import streamlit as st
# import seaborn as sns
import datetime
import pickle
import matplotlib.pyplot as plt

compName=""
list_of_companies=[]
@st.cache_resource
def loadData(): 
 global list_of_companies
 df2=pd.read_csv('pages/archive 2/NIFTY50_all.csv')

 list_of_companies=df2['Symbol'].unique()
  

 df2['Symbol'][df2['Symbol']=='HINDALC0']='HINDALCO'
 df2['Symbol'][df2['Symbol']=='HINDLEVER']='HINDUNILVR'
 df2['Symbol'][df2['Symbol']=='BHARTI']='BHARTIARTL'
 df2['Symbol'][df2['Symbol']=='KOTAKBANK']='KOTAKMAH'
 df2['Symbol'][df2['Symbol']=='TISCO']='TATASTEEL'
 df2['Symbol'][df2['Symbol']=='UTIBANK']="AXISBANK"
 df2['Symbol'][df2['Symbol']=='ZEETELE']="ZELE"
 df2['Symbol'][df2['Symbol']=='HEROHONDA']="HEROMOTOCO"
 # df2.dropna(axis=1)
 df2['Date']=pd.to_datetime(df2['Date'])
 # df2['Date']=df2['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
 return df2
df2=loadData()
st.title('Stock Price Analysis')

available_filters=df2.columns.drop(['Date','Symbol','Series','Prev Close'])
list_of_companies=df2['Symbol'].unique()
cmpy_df={}
for c in list_of_companies:
    df=df2[df2['Symbol']==c]
    df=df.drop(['Symbol'],axis=1)
    cmpy_df[c]=df

col1,col2=st.columns(2)
op=list_of_companies[0]
with col1:
 op=st.selectbox('to view graph please select a stock',list_of_companies)
with col2:
   op2=st.selectbox('to view graph please select a stock',available_filters)
import datetime

sDate : datetime.datetime=min(cmpy_df[op]['Date'])
eDate : datetime.datetime=max(cmpy_df[op]['Date'])

date_range = st.slider("Select Date Range:", sDate.date(),eDate.date(),(sDate.date(),eDate.date()))

df=cmpy_df[op]
df=df[(df['Date'].dt.date>=date_range[0]) &(df['Date'].dt.date<=date_range[1])]

st.line_chart(df,x='Date',y=op2)

# plt.plot(cmpy_df[op]['Close'])
# plt.ylabel('Close')
# plt.xlabel(None)

for company in cmpy_df.values():
    company['Daily Return'] = company['Close'].pct_change()
compName=op
st.subheader(f'Predicted Price for {compName}')

df=cmpy_df[compName]
data = df.filter(['Close'])
dataset = data.values
training_data_len = int(np.ceil( len(dataset) * .9 ))
days=30


model = pickle.load(open(f'app/pages/trainedModel/{compName}_model.sav', 'rb'))
scaler = pickle.load(open(f'app/pages/trainedModel/{compName}_scaler.sav', 'rb'))

scaled_data = scaler.fit_transform(dataset)


test_data = scaled_data[training_data_len - days: , :]

x_test = []
y_test = dataset[training_data_len:, :]
for i in range(days, len(test_data)):
   x_test.append(test_data[i-days:i, 0])
     
x_test = np.array(x_test)

x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
print(rmse)

train = data[:training_data_len]
valid = data[training_data_len:].copy()

valid['Predictions'] = predictions



include_old=st.checkbox('Include Past Data')

# st.line_chart(valid,x='Date',y=['Close','Predictions'])
fig=plt.figure(figsize=(16,6))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price INR ', fontsize=18)
l=[ 'Val', 'Predictions','Train']

plt.plot(valid[['Close', 'Predictions']])
if include_old:
 plt.plot(train['Close'])
plt.legend(l, loc='lower right')
st.pyplot(fig)
col1, col2 = st.columns(2)
today=df['Close'].values[-1]
tommorrow=round(valid['Predictions'].values[-1],2)
col1.metric("Today", today,f"{round(df['Daily Return'].values[-1],2)}%")
col2.metric("Expected Tomorrow", tommorrow, f"{tommorrow-today}")
st.header("Historical Data")
st.write(cmpy_df[op][::-1])


