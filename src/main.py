import streamlit as st
import json
import urllib.request
import pandas as pd
import plotly.express as px
import time
from datetime import datetime
from bs4 import BeautifulSoup
import ssl

# debug SSL error
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

url = 'https://kathmandupost.com/covid19'
page = urllib.request.urlopen(url)
try:
    page = urllib.request.urlopen(url)
except:
    print("An error occured.")

soup = BeautifulSoup(page,'html.parser')


total_data = soup.find_all('span', {'class':'nepal-total'})
summary = []
for i in total_data:
  for j in i.find_all('div'):
    summary.append(j.get_text())
my_dict = {}
for i in summary:
  data = i.split(':')
  #print(data)
  stripped_data = []
  for j in data:
    stripped_data.append(j.strip())
  my_dict[stripped_data[0]] = stripped_data[1]
#print(my_dict)
for key in my_dict:
    my_dict[key] = int(my_dict[key])
del my_dict['Readmitted']
my_df = pd.DataFrame(list(my_dict.items()),columns = ['Total','Cases'])

get_id = (soup.find_all('tbody'))[1]

district_id_list = []
for tag in get_id.find_all(True,{'id':True}) :
    district_id_list.append(tag['id'])

list_of_list = list()
for i in district_id_list:
    l = soup.find('tr', {"id":i})
    my_list = []
    for j in l:
        my_list.append(j.get_text())
    #print(my_list)
    list_of_list.append(my_list)

df = pd.DataFrame(list_of_list, columns=['District', 'Confirmed', 'Deaths','Recovered','Readmitted'])

# changing the data type of confirmed and deaths columns to integer
df["Confirmed"] = pd.to_numeric(df["Confirmed"])
df["Deaths"] = pd.to_numeric(df["Deaths"])


# sorting the data by the number of confirmed cases in descending order
df = df.sort_values('Confirmed',ascending=False)

#resetting the index after sorting
df = df.reset_index(drop=True)

# removing 'recovered' and 'readmitted' column from the dataframe
df = df[['District','Confirmed','Deaths']]

#saving the file
jj = my_df
ll = df
jj.to_csv("data/summary_covid-19_data_nepal.csv",index=False)
ll.to_csv("data/district_covid-19_data_nepal.csv",index=False)


geo_df = json.load(open("data/nepal.geojson",'r'))
district_df = pd.read_csv('data/district_covid-19_data_nepal.csv')
total_df = pd.read_csv('data/summary_covid-19_data_nepal.csv')

district_and_id = {}
district_and_province = {}

district_df['District'] = district_df['District'].str.lower()

for feature in geo_df['features']:
  feature['id'] = feature['id']
  district_and_id[(feature['properties']['DISTRICT']).lower()] = feature['id']
#for feature in geo_df['features']:
  district_and_province[(feature['properties']['DISTRICT']).lower()] = feature['properties']['PROVINCE']


district_and_id['nawalparasi east'] = district_and_id['nawalpur']
del district_and_id['nawalpur']

district_and_id['tanahun'] = district_and_id['tanahu']
del district_and_id['tanahu']

district_and_id['nawalparasi west'] = district_and_id['parasi']
del district_and_id['parasi']

district_and_id['sindhupalchowk'] = district_and_id['sindhupalchok']
del district_and_id['sindhupalchok']

district_and_id['illam'] = district_and_id['ilam']
del district_and_id['ilam']

district_and_id['rukum west'] = district_and_id['western rukum']
del district_and_id['western rukum']

district_and_id['rukum east'] = district_and_id['eastern rukum']
del district_and_id['eastern rukum']

district_and_id['terhathum'] = district_and_id['tehrathum']
del district_and_id['tehrathum']

#province

district_and_province['nawalparasi east'] = district_and_province['nawalpur']
del district_and_province['nawalpur']

district_and_province['tanahun'] = district_and_province['tanahu']
del district_and_province['tanahu']

district_and_province['nawalparasi west'] = district_and_province['parasi']
del district_and_province['parasi']

district_and_province['sindhupalchowk'] = district_and_province['sindhupalchok']
del district_and_province['sindhupalchok']

district_and_province['illam'] = district_and_province['ilam']
del district_and_province['ilam']

district_and_province['rukum west'] = district_and_province['western rukum']
del district_and_province['western rukum']

district_and_province['rukum east'] = district_and_province['eastern rukum']
del district_and_province['eastern rukum']

district_and_province['terhathum'] = district_and_province['tehrathum']
del district_and_province['tehrathum']


district_df['id'] = district_df['District'].apply(lambda x: district_and_id[x])
district_df['province'] = district_df['District'].apply(lambda x: district_and_province[x])
#district_df['District'] = district_df['District'].str.capitalize()

district_df['District'] = district_df['District'].str.title()
''
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
st.markdown(f"As of now ({new_dt} UTC time), there are total of {special_format(total_conf)} confirmed cases, {special_format(active_cases)} active cases, {special_format(recovered_cases)} recovered cases, and {special_format(total_dths)} deaths in Nepal. The top 5 districts with high number of reported cases are {max_district}, {sec_highest}, {third_highest}, {fourth_highest}, and {fifth_highest}. {max_district} is leading the COVID-19 battle in Nepal with {special_format(max_conf)} confirmed cases and {special_format(max_dths)} deaths.",unsafe_allow_html=True)
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
dt_string = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
st.write("<b>Created by:</b> Dipesh Poudel",unsafe_allow_html=True)
st.write("<b>Last updated on:</b> {} UTC time".format(dt_string),unsafe_allow_html=True)
