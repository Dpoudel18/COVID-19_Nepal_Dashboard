from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time


def get_data():
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
    my_dict
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
    my_df.to_csv("summary_covid-19_data_nepal.csv",index=False)
    df.to_csv("district_covid-19_data_nepal.csv",index=False)

if __name__ == "__main__":
    get_data()
