import streamlit as st
import json
import pandas as pd
import plotly.express as px
import time
from datetime import datetime
from clean_geojson import *

st.markdown("""
<style>
body {
    color: #zzz;
    background-color: #FFFFFF;
}
</style>
    """, unsafe_allow_html=True)


st.sidebar.markdown("## COVID-19 in Nepal")
total_df['Total']= total_df['Total'].replace({'Confirmed': 'Confirmed Cases', 'Active': 'Active Cases', 'Deaths': 'Deaths', 'Recovered': 'Recovered Cases'})

total_df = total_df.rename(columns={'Total': 'Cases', 'Cases': 'Count'})

st.sidebar.write(total_df.assign(hack='').set_index('hack'))

#st.sidebar.markdown("## COVID-19 cases")
#choice = st.sidebar.radio('Pick an option', ('Total','Province 1','Province 2','Province 3','Province 4','Province 5','Province 6','Province 7'))


df = district_df[['District','Confirmed','Deaths','id','province']]

def special_format(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)

def province_plot(number,lat, long):
    new_df=df[df['province']==number]
    new_df.reset_index(drop=True)
    fig = px.choropleth_mapbox(new_df, geojson=geo_df, locations='id', color='Confirmed',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=6.3, hover_name = 'District', hover_data = {'District':False, 'Confirmed':True,'Deaths':True,'province':False,'id':False},
                           opacity=0.5, center = {"lat": lat, "lon": long})
    fig.update_layout(height=500, width=700)
    total_confirmed = new_df['Confirmed'].sum()
    total_deaths = new_df['Deaths'].sum()
    max_confirmed = new_df['Confirmed'].max()
    max_deaths = new_df['Deaths'].max()
    max_district = new_df[new_df['Confirmed']==new_df['Confirmed'].max()]['District'].iloc[0]
    st.sidebar.markdown("## Province {} cases".format(number))
    st.sidebar.write(new_df[['District','Confirmed','Deaths']].assign(hack='').set_index('hack'))
    st.markdown(f"There are {special_format(total_confirmed)} confirmed cases and {special_format(total_deaths)} deaths in Province {number}. {max_district} is leading the COVID-19 battle in Province {number} with {special_format(max_confirmed)} confirmed cases and {special_format(max_deaths)} deaths.",unsafe_allow_html=True)
    st.plotly_chart(fig)


st.title("COVID-19 cases in Nepal")
fig = px.choropleth_mapbox(district_df[['District','Confirmed','Deaths','id','province']], geojson=geo_df, locations='id', color='Confirmed',
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=5.9, hover_name = 'District',hover_data = {'District':False, 'Confirmed':True,'Deaths':True,'province':False,'id':False},
                           opacity=0.5, center = {"lat": 28.3949, "lon": 84.1240})
fig.update_layout(height=700, width=900)
st.sidebar.markdown("## COVID-19 cases by District")
st.sidebar.write(district_df[['District','Confirmed','Deaths']].assign(hack='').set_index('hack'))

total_conf = df['Confirmed'].sum()
total_dths = df['Deaths'].sum()
max_conf = df['Confirmed'].max()
max_dths = df['Deaths'].max()
max_district = df[df['Confirmed']==df['Confirmed'].max()]['District'].iloc[0]
sec_highest = df['District'].iloc[1]
third_highest = df['District'].iloc[2]
fourth_highest = df['District'].iloc[3]
fifth_highest = df['District'].iloc[4]
active_cases = total_df['Count'].iloc[1]
recovered_cases = total_df['Count'].iloc[3]
new_dt = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
st.markdown(f"As of 12/09/2020 20:07:44 UTC time, there are total of {special_format(total_conf)} confirmed cases, {special_format(active_cases)} active cases, {special_format(recovered_cases)} recovered cases, and {special_format(total_dths)} deaths in Nepal. The top 5 districts with high number of reported cases are {max_district}, {sec_highest}, {third_highest}, {fourth_highest}, and {fifth_highest}. {max_district} is leading the COVID-19 battle in Nepal with {special_format(max_conf)} confirmed cases and {special_format(max_dths)} deaths.",unsafe_allow_html=True)
st.plotly_chart(fig)



st.markdown("# COVID-19 cases in Province 1")
province_plot(1,27.2,87.5)

st.markdown("# COVID-19 cases in Province 2")
province_plot(2,26.9627,85.5612)

st.markdown("# COVID-19 cases in Province 3")
province_plot(3,27.5259,85.5612)

st.markdown("# COVID-19 cases in Province 4")
province_plot(4,28.2622,84.0167)

st.markdown("# COVID-19 cases in Province 5")
province_plot(5,28.1017,82.8533)

st.markdown("# COVID-19 cases in Province 6")
province_plot(6,29.2522,82.1659)

st.markdown("# COVID-19 cases in Province 7")
province_plot(7,29.2522,80.8987)

st.sidebar.markdown("## Cases by Province")
prov_df = df.groupby(['province']).sum()
prov_df = prov_df.rename(index={1: 'Province 1',2: 'Province 2',3: 'Province 3',4: 'Province 4',5: 'Province 5',6: 'Province 6',7: 'Province 7'})
del prov_df['id']
st.sidebar.write(prov_df)

st.write("<b>Data Source:</b> Web scrapped from <em>The Kathmandu Post</em> website",unsafe_allow_html=True)
dt_string = '12/09/2020 20:07:44 UTC time'
st.write("<b>Created by:</b> Dipesh Poudel",unsafe_allow_html=True)
st.write("<b>Last updated on:</b> {} UTC time".format(dt_string),unsafe_allow_html=True)