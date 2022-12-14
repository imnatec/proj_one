import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go

df = pd.read_csv('vehicles_us.csv')

#make manufacturer column by pulling from first word in model
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

#Cleaning up data
df['is_4wd'] = df['is_4wd'].fillna('no info')
df['paint_color'] = df['paint_color'].fillna('no info')
df['odometer'] = df['odometer'].fillna(df['odometer'].mean())
df['model_year'] = df['model_year'].fillna(df['model_year'].median())
df['cylinders'] = df['cylinders'].fillna(df['cylinders'].median())
df['cylinders'] = df['cylinders'].astype('category')
df['transmission'] = df['transmission'].astype('category')
df['fuel'] = df['fuel'].astype('category')
df['model_year'] = df['model_year'].astype('int')
df['date_posted'] = pd.to_datetime (df['date_posted'], format='%Y-%m-%d')


st.header('Cars for sale')

show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)

only_automatic = st.checkbox('Show non-automatic cars?')
if only_automatic:
    df = df.query('transmission != "automatic"')

sub_100k = st.checkbox('Want to find cars with less than 100k miles?')
if sub_100k:
    df = df.query('odometer < 100000')    




st.dataframe(df)
st.header('Price of cars compared to days listed')
st.write(px.scatter(df, x='days_listed', y='price'))
st.header('Vehicle types by Engine size')
st.write(px.histogram(df, x='cylinders', color='type'))

st.header('Histogram of manufacturer vs days listed')
st.write(px.histogram(df, x='days_listed', color='manufacturer'))

st.header('Compare the mile count on for-sale cars between manufacturers')
manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
#normalize = st.checkbox('Normalize histogram', value=True)
#if normalize:
#    histnorm = 'percent'
#else:
#    histnorm = None
st.write(px.histogram(df_filtered,
                      x='odometer',
                      nbins=30,
                      color='manufacturer',
                      #histnorm=histnorm,
                      barmode='overlay'))

