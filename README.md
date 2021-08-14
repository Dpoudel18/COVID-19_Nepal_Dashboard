# COVID-19_Nepal_Dashboard
A web app that scrapes Nepal's covid-19 data  from a website and plot various geo-maps using Plotly and Streamlit.

View demo webpage at http://covid-19-nepal.herokuapp.com/

# Source File

```
scraper.py
```
-> Web scrapes this [website](https://kathmandupost.com/covid19) and generates Nepal's Covid-19 data in a csv file.

```
clean_data.py
```
-> Cleans the messy scraped data to integrate it with the geojson file for geo-plot of Nepal.

```
covid_streamlit.py
```
-> Generates a automated web article and geo-plots using Plotly and Streamlit.


# Running the Program
To run the demo version:
```
streamlit run src/covid_streamlit.py
```
To run the live and updated version:
```
streamlit run src/main.py
```
# Dependencies
```
streamlit==0.72.0

pandas==0.23.4

beautifulsoup4==4.9.3
```
Note: *The program might misbehave in future if this scrapped [website](https://kathmandupost.com/covid19) make changes to their source code* causing inaccuracies.

