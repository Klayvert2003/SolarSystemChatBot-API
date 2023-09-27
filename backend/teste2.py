import requests
import pandas as pd

API_KEY = 'ItDkjhYlTpvsEidopdqqO46Yal8Ooi9aqfxlrtLU'
start_date = '2023-08-01'
end_date = '2023-08-06'

list_date = pd.date_range(start_date, end_date)
date_list = []
for date in list_date:
    date_list.append(str(date.date()))

earth_data = requests.get(f'http://api.nasa.gov/neo/rest/v1/feed?start_date=2023-08-01&end_date=2023-08-06&detailed=true&api_key={API_KEY}').json()
print(earth_data)
input()
next_url = earth_data.get('links').get('next')