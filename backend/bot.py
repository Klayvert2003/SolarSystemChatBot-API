import spacy
import requests
import pandas as pd

from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Bot():
    def __init__(self) -> None:
        self.nlp = spacy.load("pt_core_news_md")
        self.API_KEY = getenv('API_KEY')
        self.planet_distances_from_sun = {
            "mercurio": 57.9,
            "venus": 108.2,
            "terra": 149.6,
            "marte": 227.9,
            "jupiter": 778.3,
            "saturno": 1427,
            "urano": 2871,
            "netuno": 4497.1
        }
        self.planet_info = {
            "mercurio": {
                "desc": "Mercurio é o planeta mais próximo do Sol e não possui satélites naturais.",
                "rotação": "58,6 dias terrestres",
                "revolução": "87,97 dias terrestres",
                "diametro": "4.880 km",
                "satelites": []
            },
            "venus": {
                "desc": "Venus é similar em tamanho à Terra, mas tem uma atmosfera densa e é muito quente.",
                "rotação": "243 dias terrestres",
                "revolução": "224,7 dias terrestres",
                "diametro": "12.104 km",
                "satelites": []
            },
            "terra": {
                "desc": "A Terra é nosso lar! O único planeta conhecido que possui vida.",
                "rotação": "24 horas",
                "revolução": "365,25 dias",
                "diametro": "12.742 km",
                "satelites": ["lua"]
            },
            "marte": {
                "desc": "Marte, conhecido como o planeta vermelho.",
                "rotação": "24,6 horas",
                "revolução": "687 dias terrestres",
                "diametro": "6.779 km",
                "satelites": ["fobos", "deimos"]
            },
            "jupiter": {
                "desc": "Júpiter é o maior planeta do sistema solar.",
                "rotação": "9,9 horas",
                "revolução": "4.331,5 dias terrestres",
                "diametro": "139.820 km",
                "satelites": ["io", "europa", "ganimedes", "calisto"]
            }
        }
        self.satelite_info = {
            "lua": "A Lua é o único satélite natural da Terra.",
            "fobos": "Fobos é um dos dois satélites de Marte e é o maior deles.",
            "deimos": "Deimos é um dos dois satélites de Marte e é o menor deles.",
            "io": "Io é um dos quatro maiores satélites de Júpiter e é conhecido por sua atividade vulcânica.",
            "europa": "Europa é um dos quatro maiores satélites de Júpiter e é conhecido por ter um oceano subterrâneo.",
            "ganimedes": "Ganimedes é o maior satélite de Júpiter e é maior do que o planeta Mercúrio.",
            "calisto": "Calisto é um dos quatro maiores satélites de Júpiter e é notável por sua superfície fortemente craterizada."
        }
        super().__init__()

    def chatbot_response(self, text):
        text = text.lower()

        for planet, info in self.planet_info.items():
            if planet in text:
                if "satélites" in text or "luas" in text or "satelite" in text:
                    if info["satelites"]:
                        return f"Os principais satélites de {planet.capitalize()} são: {', '.join(info['satelites'])}."
                    else:
                        return f"{planet.capitalize()} não possui satélites naturais."
                if "rotação" in text:
                    return f"A rotação de {planet.capitalize()} é de {info['rotação']}."
                elif "revolução" in text:
                    return f"A revolução de {planet.capitalize()} é de {info['revolução']}."
                elif "diametro" in text:
                    return f"O diâmetro de {planet.capitalize()} é de {info['diametro']}."

        # Distância entre dois planetas
        planets_in_query = [planet for planet in self.planet_distances_from_sun if planet in text]
        if ("distância" in text or "entre" in text) and len(planets_in_query) == 2:
            planet_1, planet_2 = planets_in_query
            distance = abs(self.planet_distances_from_sun[planet_1] - self.planet_distances_from_sun[planet_2])
            return f"A distância média entre {planet_1.capitalize()} e {planet_2.capitalize()} é de {distance} milhões de km."

        # Descrições gerais de um planeta ou satélite
        for planet, info in self.planet_info.items():
            if planet in text:
                return info["desc"]
        for satelite, desc in self.satelite_info.items():
            if satelite in text:
                return desc

        return "Desculpe, não consegui entender. Por favor, reformule ou faça outra pergunta."
    
    def get_asteroid_info(self, start_date, end_date):
        list_date = pd.date_range(start_date, end_date)
        asteroid_info_list = []

        for date in list_date:
            date = str(date).split()[0]
            url = f'http://api.nasa.gov/neo/rest/v1/feed?start_date={date}&end_date={date}&detailed=true&api_key={self.API_KEY}'
            asteroid_data = requests.get(url).json()

            if date in asteroid_data["near_earth_objects"]:
                asteroids = asteroid_data["near_earth_objects"][date]

                for asteroid in asteroids:
                    name = asteroid["name"]
                    min_diameter = asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
                    max_diameter = asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"]
                    is_potentially_hazardous = asteroid["is_potentially_hazardous_asteroid"]

                    asteroid_info = {
                        "name": name,
                        "date": date,
                        "min_diameter": min_diameter,
                        "max_diameter": max_diameter,
                        "is_potentially_hazardous": is_potentially_hazardous
                    }

                    asteroid_info_list.append(asteroid_info)

        if asteroid_info_list:
            return asteroid_info_list
        else:
            return "Desculpe, não consegui encontrar informações sobre asteroides nessas datas."
