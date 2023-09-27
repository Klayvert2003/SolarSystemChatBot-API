import requests
import pandas as pd

API_KEY = "ItDkjhYlTpvsEidopdqqO46Yal8Ooi9aqfxlrtLU"
def get_asteroid_info(start_date, end_date):
    list_date = pd.date_range(start_date, end_date)
    asteroid_info_list = []

    for date in list_date:
        date = str(date).split()[0]
        url = f'http://api.nasa.gov/neo/rest/v1/feed?start_date={date}&end_date={date}&detailed=true&api_key={API_KEY}'
        asteroid_data = requests.get(url).json()

        if date in asteroid_data["near_earth_objects"]:
            asteroids = asteroid_data["near_earth_objects"][date]

            for asteroid in asteroids:
                name = asteroid["name"]
                min_diameter = asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
                max_diameter = asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
                is_potentially_hazardous = asteroid["is_potentially_hazardous_asteroid"]

                info = f"Informações sobre o asteroide {name} ({date}):\n"
                info += f"Diâmetro estimado: De {min_diameter:.2f} km a {max_diameter:.2f} km.\n"
                if is_potentially_hazardous:
                    info += "Este asteroide é potencialmente perigoso para a Terra.\n"
                else:
                    info += "Este asteroide não é potencialmente perigoso para a Terra.\n"

                asteroid_info_list.append(info)

    if asteroid_info_list:
        return "\n".join(asteroid_info_list)
    else:
        return "Desculpe, não consegui encontrar informações sobre asteroides nessas datas."


asteroid_info = get_asteroid_info('2023-08-01', '2023-08-06')