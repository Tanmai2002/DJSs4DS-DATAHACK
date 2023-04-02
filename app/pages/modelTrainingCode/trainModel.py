import pandas as pd
import numpy as np
import pickle
df2=pd.read_csv('/Users/muskaansharma/Desktop/ZcodersDatahack/app/pages/archive 2/NIFTY50_all.csv')

list_of_companies=df2['Symbol'].unique()

df2['Symbol'][df2['Symbol']=='HINDALC0']='HINDALCO'
df2['Symbol'][df2['Symbol']=='HINDLEVER']='HINDUNILVR'
df2['Symbol'][df2['Symbol']=='BHARTI']='BHARTIARTL'
df2['Symbol'][df2['Symbol']=='KOTAKBANK']='KOTAKMAH'
df2['Symbol'][df2['Symbol']=='TISCO']='TATASTEEL'
df2['Symbol'][df2['Symbol']=='UTIBANK']="AXISBANK"
df2['Symbol'][df2['Symbol']=='ZEETELE']="ZELE"
df2['Symbol'][df2['Symbol']=='HEROHONDA']="HEROMOTOCO"

list_of_companies=df2['Symbol'].unique()
cmpy_df={}
for c in list_of_companies:
    df=df2[df2['Symbol']==c]
    df=df.drop(['Symbol'],axis=1)
    cmpy_df[c]=df

def trainModel(compName):
    df=cmpy_df[compName]
    data = df.filter(['Close'])
    dataset = data.values
    training_data_len = int(np.ceil( len(dataset) * .8 ))
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    filename = f'app/pages/trainedModel/{compName}_scaler.sav'
    pickle.dump(scaler, open(filename, 'wb')) 

    scaled_data
    
    train_data = scaled_data[0:int(training_data_len), :]
    days=30
    x_train = []
    y_train = []

    for i in range(days, len(train_data)):
        x_train.append(train_data[i-days:i, 0])
        y_train.append(train_data[i, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    from keras.models import Sequential
    from keras.layers import Dense, LSTM
    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(150, return_sequences=True, input_shape= (x_train.shape[1], 1)))
    model.add(LSTM(80, return_sequences=False))
    model.add(Dense(35))
    model.add(Dense(12))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=1, epochs=1)
    filename = f'app/pages/trainedModel/{compName}_model.sav'
    pickle.dump(model, open(filename, 'wb')) 
for i in list_of_companies:
    trainModel(i)