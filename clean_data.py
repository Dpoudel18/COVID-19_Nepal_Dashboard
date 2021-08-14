import streamlit as st
import json
import pandas as pd
import plotly.express as px
import time
from datetime import datetime



geo_df = json.load(open("nepal.geojson",'r'))
district_df = pd.read_csv('district_covid-19_data_nepal.csv')
total_df = pd.read_csv('summary_covid-19_data_nepal.csv')

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