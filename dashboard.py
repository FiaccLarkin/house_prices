import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

data = pd.read_csv(os.path.join(dir_path, 'data.csv'), index_col='date')
data.index = pd.to_datetime(data.index)
data.index = data.index.map(lambda x: x.date())

data['pos'] = ((data['change'] > 0)*2)-1
data['order'] = range(len(data))

data.sort_values('location', inplace=True)

data.loc[data['location'] == 'Whole Country', 'order'] = -2
data.loc[data['location'] == 'Limerick City', 'order'] = -1

data['wide area'] = ''
data['wide area'] = data['wide area'].where(data['location'].apply(lambda x: 'imerick' not in x), 'Limerick')
data['wide area'] = data['wide area'].where(data['location'].apply(lambda x: 'ublin' not in x), 'Dublin')
data['wide area'] = data['wide area'].where(data['location'].apply(lambda x: 'ork' not in x), 'Cork')

# Location selection
data.sort_values('order', ascending=True, inplace=True)
locations = data['wide area'].unique().tolist()
locations = locations + ['Whole Country']
selected_location = st.sidebar.selectbox('location', locations)

# Date range selection
data.index = pd.to_datetime(data.index)
data.sort_index(inplace=True)
start_date = st.sidebar.date_input('start date', data.index[0])
end_date = st.sidebar.date_input('end date', data.index[-1])
data = data.loc[start_date:end_date]

st.title(f'Property Price Changes - {selected_location}')

if selected_location == 'Whole Country':
    subset = data
else:
    subset = data[data['wide area'] == selected_location]

fig, ax = plt.subplots()
change_mean = subset.groupby('date')['change'].mean()
change_mean.plot(kind='bar', title='mean percentage change', color='b')
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots()
change_mean.cumsum().plot(title='cummulative sum', color='r')
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots()
pos_sum = subset.groupby('date')['pos'].sum()
pos_sum.plot(kind='bar', title='up/down sum', color='y')
plt.tight_layout()
st.pyplot(fig)



